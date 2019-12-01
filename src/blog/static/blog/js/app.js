$(document).ready( () => {
  $(".content-markdown").forEach( () => {
    let content = $(this).text();
    console.log(content);
    let markedContent = marked(content);
    $(this).html(markedContent);
  });
  $(".content-markdown img").forEach( () => {
    $(this).addClass("img-responsive")

  });
});
