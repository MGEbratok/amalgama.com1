$(document).ready(function(){
    $(document).on("click", ".dropdown-icon", function(e){
    e.preventDefault()
    document.getElementByld(".dropdown").classList.toggle("hidden");  
    });
    $(document).on("click", ".delete", function(e){
    e.preventDefault()
    var post_id =$(this).data("post_id")
    console.log(post_id)
    $ajax({
                url: url,
                type: "POST",
                data: {
                    post_id: post_id,
                    csrfmiddlewaretoken: $("input[name=iddlewaretoken]").val(),
                },
                cache: true,
                success: function (data) {
                    console.log("OK");

                },
                error: function() {
                    console.log("error");
                }
        });
    });
});