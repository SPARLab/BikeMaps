$(function(){
  $('#italics-btn').click(function(e){
    // appendToContent(' *italic*');
    insertAtCaret('id_content',' *italic*')
  })
  $('#bold-btn').click(function(e){
    // appendToContent(' **bold**');
    insertAtCaret('id_content',' **bold**')
  })
  $('#list-btn').click(function(e){
    // appendToContent('\n- list item');
    insertAtCaret('id_content','\n- list item')
  })
  $('#link-btn').click(function(e){
    // appendToContent(' [link](http://url.com)');
    insertAtCaret('id_content',' [link](http://url.com)')
  })

  $('#upload-image-form').submit(upload);
})

function appendToContent(text){
  $('#id_content').val($('#id_content').val() + text)
}

function insertAtCaret(areaId, text) {
    var txtarea = document.getElementById(areaId);
    var scrollPos = txtarea.scrollTop;
    var strPos = 0;
    var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
        "ff" : (document.selection ? "ie" : false ) );
    if (br == "ie") {
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
    }
    else if (br == "ff") strPos = txtarea.selectionStart;

    var front = (txtarea.value).substring(0,strPos);
    var back = (txtarea.value).substring(strPos,txtarea.value.length);
    txtarea.value=front+text+back;
    strPos = strPos + text.length;
    if (br == "ie") {
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        range.moveStart ('character', strPos);
        range.moveEnd ('character', 0);
        range.select();
    }
    else if (br == "ff") {
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
    }
    txtarea.scrollTop = scrollPos;
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
