$(document).ready( () => {

  const btn = $('#back-to-top-button');

  $(window).scroll(function() {
    if ($(window).scrollTop() > 300) {
      btn.addClass('show');
    } else {
      btn.removeClass('show');
    }
  });

  btn.on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop:0}, '300');
  });



  // $(window).scroll(function() { // check if scroll event happened
  //   if ($(document).scrollTop() > 50) { // check if user scrolled more than 50 from top of the browser window
  //     $(".navbar").css("background-color", "#f4f4f4"); // if yes, then change the color of class "navbar-fixed-top" to white (#f8f8f8)
  //   } else {
  //     $(".navbar").css("background-color", "transparent"); // if not, change it back to transparent
  //   }
  // });

  // $(".content-markdown").each(function() {
  //   let content = $(this).text();
  //   let markedContent = marked(content);
  //   $(this).html(markedContent);
  // });

  $(".post-detail-item img").each(function() {
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
