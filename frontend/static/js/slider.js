var slider_text = {
    1: ['One word','One Hour'],
    2: ['Two words','Twelve Hours'],
    3: ['Three words','Two Days'],
    4: ['Four words','One Week'],
}

function populate_slider_text(value){
    /* Given the current value of the slider, populate the slider text divs */
    var text = slider_text[value];
    $('#slider_left_text').text(text[0]);
    $('#slider_right_text').text(text[1]);
}

$(document).ready(function() {
    var select = $("#id_duration");
    var slider = $("#slider").slider({
        min: 1,
        max: 4,
        range: "min",
        value: select[ 0 ].selectedIndex + 1,
        slide: function( event, ui ) {
            select[ 0 ].selectedIndex = ui.value - 1;
            populate_slider_text(ui.value);
        }
    });
    $( "#id_duration" ).change(function() {
        populate_slider_text(this.selectedIndex + 1);
        slider.slider( "value", this.selectedIndex + 1 );
    });
    select.parent().hide(); /* Hide parent to ensure that icon is hidden as well */
    populate_slider_text(select[0].selectedIndex + 1);
});