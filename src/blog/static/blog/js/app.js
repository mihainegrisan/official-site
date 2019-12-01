$(document).ready( () => {
  $(".content-markdown").each(function() {
    let content = $(this).text();
    console.log(content);
    let markedContent = marked(content);
    $(this).html(markedContent);
  });
  $(".content-markdown img").each(function() {
    $(this).addClass("img-fluid")
  });
});
