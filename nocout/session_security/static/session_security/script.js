/*Initialize the timer*/
var timer = "";
var count = 1;
// Use 'yourlabs' as namespace.
if(window.yourlabs == undefined) window.yourlabs = {};

// Session security constructor. These are the required options:
//
// - pingUrl: url to ping with last activity in this tab to get global last
//   activity time,
// - warnAfter: number of seconds of inactivity before warning,
// - expireAfter: number of seconds of inactivity before expiring the session.
//
// Optional options:
//
// - confirmFormDiscard: message that will be shown when the user tries to
//   leave a page with unsaved form data. Setting this will enable an
//   onbeforeunload handler that doesn't block expire().
// - events: a list of event types to watch for activity updates.
yourlabs.SessionSecurity = function (options) {

    var that = this;
    /*Assign the default value to the timer*/
    timer = 10;

    // **HTML element** that should show to warn the user that his session will
    // expire.    
    this.$warning = $('#session_security_warning');

    // Last recorded activity datetime.
    this.lastActivity = new Date();

    // Events that would trigger an activity
    this.events = ['mousemove', 'scroll', 'keyup', 'click'];

    // Merge the options dict here.
    $.extend(this, options);

    /*Bind the click event on 'Continue' button.*/
    $("#sessionContinue").click(function (e) {

        that.continueFunction(e);
    });
    /*Bind the click event on 'logoutFunction' button.*/
    $("#sessionLogout").click(function (e) {

        that.logoutFunction(e);
    });

    // Bind activity events to update this.lastActivity.
    for (var i = 0; i < this.events.length; i++) {
        $(document)[this.events[i]]($.proxy(this.activity, this))
    }

    // Initialize timers.
    this.apply("");

    if(this.confirmFormDiscard) {
        window.onbeforeunload = $.proxy(this.onbeforeunload, this);
        $(document).on('change', ':input', $.proxy(this.formChange, this));
        $(document).on('submit', 'form', $.proxy(this.formSubmit, this));
    }
}

yourlabs.SessionSecurity.prototype = {
    // Called when there has been no activity for more than expireAfter
    // seconds.
    expire: function () {
        this.expired = true;
        setTimeout(window.location.reload(), 1000);
    },

    // Called when there has been no activity for more than warnAfter
    // seconds.
    showWarning: function (countdown) {

        this.$warning.fadeIn('slow');

        // $(".session_security_overlay").css("height", window.height+"px");

        if(countdown) {
            this.startCountdown(timer);
        } else {
            this.startCountdown(0);
        }
    },

    // Called to hide the warning, for example if there has been activity on
    // the server side - in another browser tab.
    hideWarning: function () {

        /*Reset the timer counter to initial value*/
        timer = 10;

        /*hide the dialog*/
        this.$warning.hide();
    },

    // Called by click, scroll, mousemove, keyup.
    activity: function () {


        var isVisible = $("#session_security_warning").attr("style");
        if(isVisible != undefined) {
            this.lastActivity = new Date();
            if(this.$warning.is(':visible')) {
                // Inform the server that the user came back manually, this should
                // block other browser tabs from expiring.
                this.ping();
            }
            // this.hideWarning();
        }
    },

    // Hit the PingView with the number of seconds since last activity.
    ping: function () {
        var idleFor = Math.floor((new Date() - this.lastActivity) / 1000);
        if(idleFor) {
            $.ajax(this.pingUrl, {
                data: {idleFor: idleFor},
                cache: false,
                success: $.proxy(this.pong, this),
                // In case of network error, we still want to hide potentially
                // confidential data !!
                error: $.proxy(this.apply, this),
                dataType: 'json',
                type: 'get'
            });
        } else {
            $.proxy(this.apply, this)
        }
    },

    // Callback to process PingView response.
    pong: function (data) {
        if(data == 'logout') return this.expire();

        this.lastActivity = new Date();
        this.lastActivity.setSeconds(this.lastActivity.getSeconds() - data);
        this.apply("");
    },

    // Apply warning or expiry, setup next ping
    apply: function (keyVal) {
        //we have single user single session
        // this change ensures that if somebidy else logs in
        // the user is logged off and redirected

        if(keyVal.statusText === "error") {
            this.showWarning(false);
        }

        // Cancel timeout if any, since we're going to make our own
        clearTimeout(this.timeout);

        var idleFor = Math.floor((new Date() - this.lastActivity) / 1000);

        nextPing = 5;

        if(idleFor >= this.expireAfter) {
            timer = this.expireAfter - idleFor;
            this.showWarning(false);
        } else if(idleFor >= this.warnAfter) {
            timer = this.expireAfter - idleFor;
            this.showWarning(true);
        } else {
            // this.hideWarning();
            nextPing = this.warnAfter - idleFor;
            timer = this.expireAfter - nextPing;
        }

        this.timeout = setTimeout($.proxy(this.ping, this), nextPing * 1000);
    },

    // onbeforeunload handler.
    onbeforeunload: function (e) {
        if($('form[data-dirty]').length && !this.expired) {
            return this.confirmFormDiscard;
        }
    },

    // When an input change, set data-dirty attribute on its form.
    formChange: function (e) {
        $(e.target).closest('form').attr('data-dirty', true);
    },

    // When a form is submited, unset data-dirty attribute.
    formSubmit: function (e) {
        $(e.target).removeAttr('data-dirty');
    },
    /*Triggers when 'Continue' button is clicked*/
    continueFunction: function (e) {

        this.apply("");
        this.hideWarning();
    },
    /*Triggers when 'Logout' button is clicked*/
    logoutFunction: function (e) {
        var logout_url = window.location.origin+"/logout/"
        window.location.href = logout_url;
    },
    /*To show the countdown on the dialog*/
    startCountdown: function (timer) {

        if(timer > 0) {
            $("#counterVal > h1").html(timer + ' <i class="fa fa-clock-o">&nbsp;</i>');
        } else {
            $("#session_bottom_content").hide();
            $("#counterVal > h1").html("Session has expired, due to inactivity or this account has been logged in from a new location.");
            
            var current_this = this;

            setTimeout(function() {
                current_this.expire();
            }, 1500);
        }
    }
};
