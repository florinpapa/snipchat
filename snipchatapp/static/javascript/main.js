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
  save.on('click', function(e) {
    var identifier = location.href.match(/[a-zA-Z0-9]{6}/g).pop();
    saveSnippet(e, location.origin + '/snippet/update/' + identifier + '/');
  });

  var add = $('#submit');
  add.on('click', function(e) {
    saveSnippet(e, location.origin + '/snippet/add_snippet/');
  });

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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

  function saveSnippet(e, url) {
    e.preventDefault();

    var code = editor.getSession().getValue();
    $.post(url, {
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

  function commentsOnRow(row) {
    return function(comment) {
      return comment.row == row;
    };
  }

  function addCommentForm(top, row, data) {
    var $commentContainer = $(data);
    if (row >= 0) {

      var comments = parseEditorComments()
                     .filter(function(c) {return c.row == row;});
                         
      $commentContainer.css("top", top - 70);
      $form = $('form', $commentContainer);
      $submit = $('#submit', $form);
      $cancel = $('#cancel', $form);
      $submit.on('click', addInlineComment.bind($form, row));
      $cancel.on('click', cancelComment.bind($form));
      $('#editor').append($commentContainer);

      $('.code-comment').each(function(idx, comment) {
        var r = parseInt($('.row', comment).text());
        if (r == row) {
          $('.inline-comment_container').prepend($(comment).clone());
        }
      });
    
    }
  }

  function cancelComment(e) {
    e.preventDefault();
    this.parent().remove();
  }

  function addInlineComment(row, e) {
    e.preventDefault();

    var $this = $(this),
        url = location.origin + '/snippet' + $this.attr('action'),
        comment = $('textarea', $this).val(),
        token = $('input[name=csrfmiddlewaretoken]', $this).val();

    if (!comment.length) {
      return;
    }

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

  function parseEditorComments() {
    var comments = $('.code-comment');
    var annotations = [];
    comments.each(function(idx, ref) {
      var $ref = $(ref);
      annotations.push({
        row: parseInt($('.row', $ref).text()),
        column: 0,
        text: $('.comment', $ref).text().trim(),
        type: "warning"
      });
    });
    return annotations;
  }

  function renderEditorComments() {
    editor.getSession()
        .setAnnotations(parseEditorComments());
  }

  renderEditorComments();


})();
