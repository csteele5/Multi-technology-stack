
    // Example starter JavaScript for disabling form submissions if there are invalid fields
    (function() {
        'use strict';
        window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
            }, false);
        });
        }, false);
    })();
    
$(document).ready(function(){
    
    //alert('snippet js ready.  This is the correct file from the snippets application!!!');
    snippetID = $("#inputSnippetID").val();
    //alert("snippet ID "+snippetID);

    if (snippetID > 0) {
        $("#btnEdit").removeClass('d-none');
    }

    $("#btnEdit").click(function() {
        $(this).addClass("d-none");
        $("#btnUpdate").removeClass('d-none');
        $("#btnDeleteSnippet").removeClass('d-none');

        $("#inputTitle").attr("readonly", false);
        $("#inputCode").attr("readonly", false);
        $("#inputLanguage").attr("readonly", false);
        $("#inputStyle").attr("readonly", false);
        //$("#inputOwner").attr("readonly", false); // cannot change owner from edit - need to go to admin
        $("#inputLinenos").attr("readonly", false);

        $("#inputLanguage").attr("disabled", false);
        $("#inputStyle").attr("disabled", false);
        //$("#inputOwner").attr("disabled", false);
        $("#inputLinenos").attr("disabled", false);

    })
    

    $("#btnCreateSnippetFromSnippet").click(function() {
        //alert('submit!');
        language = $("#inputLanguage").val();
        $("#newlanguage").val(language);
        style = $("#inputStyle").val();
        $("#newstyle").val(style);
        $( "#createNewSnippetForm" ).submit();
    })

    

    $("#btnCreateSnippetFromList").click(function() {
        //alert('submit!');
        language = $("#filter_language").val();
        $("#newlanguage").val(language);
        $( "#createNewSnippetForm" ).submit();

    })

    $("#btnDeleteSnippet").click(function() {
        //alert('submit!');
        $( "#deleteSnippetForm" ).submit();

    })

    $("#btnCreateSnippetx").click(function() {
        //alert('submit!');
       
        submitForm = 1;
        title = $("#inputTitle").val();
        code = $("#inputCode").val();
        language = $("#inputLanguage").val();
        style = $("#inputStyle").val();

        if (title == '') {
            alert('test validation - title');
            submitForm = 0;
        }
        if (code == '') {
            alert('test validation - code');
            submitForm = 0;
        }
        if (language == '') {
            alert('test validation - language');
            submitForm = 0;
        }
        if (style == '') {
            alert('test validation - style');
            submitForm = 0;
        }
        if (submitForm == 1) {
            $( "#newSnippetForm" ).submit();
        }
        

    })
    


    $("#filter_all_languages").click(function() {
        //alert('filter!');
        $(this).closest('form').submit();

    })



    $(".return_to_snippet_list_post_link").click(function(){
        //alert('click');
        language = $("#inputLanguage").val();
        style = $("#inputStyle").val();

        $("#filter_language").val(language);
        $("#filter_style").val(style);


        $( "#returntolistform" ).submit();
    
    });
    
});