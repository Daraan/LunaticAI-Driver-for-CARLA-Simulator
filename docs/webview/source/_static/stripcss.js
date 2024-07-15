// disables external_icon.css on code pages
const disable_conditions = ["agents", "classes", "data_gathering", "AgentGameLoop.html"]

$(function () {
    if ( disable_conditions.some(cond => location.pathname.indexOf(cond) >= 0) ) {
        for ( i=0; i<document.styleSheets.length; i++) {
            var sheet = document.styleSheets.item(i);
            if (sheet.href && sheet.href.includes('external_icon.css')){
                sheet.disabled = true;
                console.log("disabled custom.css on " + location);
            }
        }
    }
});