
$(document).ready(function(){
    alert('snippet js ready');


    $(".return_to_snippet_list_post_link").click(function(){
        alert('click');
        $( "#returntolistform" ).submit();
    
    });
    
});