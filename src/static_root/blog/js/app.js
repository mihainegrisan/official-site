$(document).ready( () => {
  $(".content-markdown").each(function() {
    let content = $(this).text();
    let markedContent = marked(content);
    $(this).html(markedContent);
  });

  $(".content-markdown img").each(function() {
    $(this).addClass("img-fluid");
  });


  // AUTO MARKDOWN PREVIEW

  // CONTENT

  const contentInput = $("#id_content");
  // $("#preview-content").html(marked(contentInput.val()));

  function setContent(value) {
    let markedContent = marked(value);
    $("#preview-content").html(markedContent);
    $("#preview-content img").each(function() {
      $(this).addClass("img-fluid");
    });
  }

  setContent(contentInput.val());

  contentInput.keyup(function() {
    newContent = $(this).val();
    setContent(newContent);
  });

  // TITLE

  const titleInput = $("#id_title");
  // $("#preview-title").text(titleItem.val());

  function setTitle(value) {
    $("#preview-title").text(value);
  }

  setTitle(titleInput.val());

  titleInput.keyup(function() {
    newTitle = $(this).val();
    setTitle(newTitle);
  });

});
