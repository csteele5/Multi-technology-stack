
$(document).ready(function(){
    alert('snippet js ready.  This is the correct file from the snippets application!!!');


    $(".return_to_snippet_list_post_link").click(function(){
        alert('click');
        $( "#returntolistform" ).submit();
    
    });
    
});