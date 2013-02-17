/* This needs to be minified and then added into templates/bookmarklet/html */

var api_endpoint = 'http://helpfulpenguin.com/redirects/';
var post_data = {
    "url":window.location.href,
    "duration":"3"
};
$.ajax({
    url: api_endpoint,
    data: post_data,
    type: 'POST',
    dataType: 'json',
}).success(
    function(response){
        alert("Your temporary link is www.helpfulpenguin.com/" + response.slug);
    });