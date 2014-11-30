(function() {


  if ($('#editor').length) {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/twilight");
    editor.getSession().setMode("ace/mode/c_cpp");
    editor.on("gutterclick", function(e) {
      var url = location.origin + '/snippet/inline_comment_html/';
      var identifier = location.href.match(/[a-zA-Z0-9]{6}/g).pop();
      var row = getLineNumber(e);
      $.post(url, {snippet_id: identifier})
      .success(addCommentForm.bind(this, e.y, row))
      .fail(function(data) { console.log(data); });
    });
  }

  var save = $('#save');
  save.on('click', saveVersion);

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        var csrf = $('input[name=csrfmiddlewaretoken]').val();
        var csrftoken = getCookie('csrftoken') || csrf;
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  function saveVersion(e) {
    e.preventDefault();

    var code = editor.getSession().getValue();
    var identifier = location.href.match(/[a-zA-Z0-9]{6}/g).pop();
    $.post('http://localhost:8000/snippet/update/' + identifier + '/', {
      code: code,
    }).success(function(data) {
      console.log(data);
      window.location.href = location.origin + "/snippet/" + data.identifier;
    }).fail(function(data) {
      console.log(data);
    });
  }

  function getLineNumber(e) {
    var target = e.domEvent.target;
    if (target.className.indexOf("ace_gutter-cell") == -1)
      return;
    if (!editor.isFocused())
      return;
    if (e.clientX > 25 + target.getBoundingClientRect().left)
      return;

    var row = e.getDocumentPosition().row;
    return row;
  }

  function addCommentForm(top, row, data) {
    var $commentContainer = $(data);
    if (row >= 0) {
      $commentContainer.css("top", top - 77);
      $form = $('form', $commentContainer);
      $form.on('submit', addInlineComment.bind($form, row));
      $('#editor').append($commentContainer);
    }
  }

  function addInlineComment(row, e) {
    e.preventDefault();
    var $this = $(this);
    var url = location.origin + '/snippet' + $this.attr('action');
    var comment = $('textarea', $this).val();
    var token = $('input[name=csrfmiddlewaretoken]', $this).val();
    $.post(url, {
      csrfmiddlewaretoken: token,
      comment: comment,
      row: row
    }).success(function(data) {
      if (data.success === 'false') {
        location.href = location.origin + '/snippet/register/';
      }
    }).fail(function(data) {
      console.log(data);
    });
  }

  function renderEditorComments() {
    var comments = $('.code-comment');
    comments.each(function(idx, ref) {
      var $ref = $(ref);
      editor.getSession().setAnnotations([{
        row: parseInt($('.row', $ref).text()),
        column: 10,
        text: $('.comment', $ref).text(),
        type: "warning"
      }]);
    });
  }

  renderEditorComments();


})();
