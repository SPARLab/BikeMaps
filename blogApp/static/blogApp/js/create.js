$(function(){
  $('#italics-btn').click(function(e){
    appendToContent(' *italic*');
  })
  $('#bold-btn').click(function(e){
    appendToContent(' **bold**');
  })
  $('#list-btn').click(function(e){
    appendToContent('\n- list item');
  })
  $('#link-btn').click(function(e){
    appendToContent(' [link](http://url.com)');
  })

  $('#upload-image-form').submit(upload);
})

function appendToContent(text){
  $('#id_content').val($('#id_content').val() + text)
}

function upload(event) {
  event.preventDefault();
  var data = new FormData($('#upload-image-form').get(0));

  $.ajax({
      url: $(this).attr('action'),
      type: $(this).attr('method'),
      data: data,
      cache: false,
      processData: false,
      contentType: false,
      success: function(data) {
        if (!(data['success'])) {
          $("#img-form-crispy").replaceWith(data['form_html']);
        }
        else {
          $('#upload-image-form #submit-id-save').prop('disabled', false);
          appendToContent(' !['+ data.title +']('+ data.url +')');
          // appendToContent(' <img class="img-responsive" alt="'+ data.title +'" src="'+ data.url +'"/>');
          $('#upload-img-modal').modal('hide');
        }
      }

  });
  return false;
}
