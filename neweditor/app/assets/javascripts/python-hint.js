(function () {
  function forEach(arr, f) {
    for (var i = 0, e = arr.length; i < e; ++i) f(arr[i]);
  }

  function arrayContains(arr, item) {
    if (!Array.prototype.indexOf) {
      var i = arr.length;
      while (i--) {
        if (arr[i] === item) {
          return true;
        }
      }
      return false;
    }
    return arr.indexOf(item) != -1;
  }

  function scriptHint(editor, _keywords, getToken) {
    // Find the token at the cursor
    var cur = editor.getCursor(), token = getToken(editor, cur), tprop = token;
    // If it's not a 'word-style' token, ignore the token.

    if (!/^[\w$_]*$/.test(token.string)) {
        token = tprop = {start: cur.ch, end: cur.ch, string: "", state: token.state,
                         className: token.string == ":" ? "python-type" : null};
    }

    if (!context) var context = [];
    context.push(tprop);

    var completionList = getCompletions(token, context);
    completionList = completionList.sort();
    //prevent autocomplete for last word, instead show dropdown with one word
    if(completionList.length == 1) {
      completionList.push(" ");
    }

    return {list: completionList,
            from: CodeMirror.Pos(cur.line, token.start),
            to: CodeMirror.Pos(cur.line, token.end)};
  }

  CodeMirror.pythonHint = function(editor) {
    return scriptHint(editor, pythonKeywordsU, function (e, cur) {return e.getTokenAt(cur);});
  };



  var pythonKeywords = "and or xor not while as elif global else if"
+ "break include class in return fun for true True false False do end new each for\ each\ element\ in\ list\ do\n\ statement\n\ end ";
  var pythonKeywordsL = pythonKeywords.split(" ");
  var pythonKeywordsU = pythonKeywords.toUpperCase().split(" ");

  var pythonBuiltins = "pdf print @ ";
  var pythonBuiltinsL = pythonBuiltins.split(" ").join("() ").split(" ");
  var pythonBuiltinsU = pythonBuiltins.toUpperCase().split(" ").join("() ").split(" ");

  function getCompletions(token, context) {
    var found = [], start = token.string;
    function maybeAdd(str) {
      if (str.indexOf(start) == 0 && !arrayContains(found, str)) found.push(str);
    }

    ////////////////////////////////////////////////////////////////
    // Custom long builtins added here
    ////////////////////////////////////////////////////////////////
    
    //basic for loop
    pythonBuiltinsL.push("for element in list do\n" + 
    "    statement;\n" +
    "end");

    //if statements
    pythonBuiltinsL.push("if(condition) do\n" + 
    "    statements;\n" +
    "end");
    pythonBuiltinsL.push("elif(condition) do\n" + 
    "    statements;\n");
    pythonBuiltinsL.push("else\n" + 
    "    statements;\n");



    // Class definition
    pythonBuiltinsL.push("class classname do\n" + 
    "    #class body goes here\n" +
    "end");

    // imports
    pythonBuiltinsL.push("include libname;");


    //assignments
    pythonBuiltinsL.push("var = [element1, element2, ..., elementn];");
    pythonBuiltinsL.push("var = {key1:value1, key2:value2, ..., key2:value2};");












    ////////////////////////////////////////////////////////////////
    // Custom long builtins ends here
    ////////////////////////////////////////////////////////////////


    function gatherCompletions(_obj) {
        forEach(pythonBuiltinsL, maybeAdd);
        forEach(pythonBuiltinsU, maybeAdd);
        forEach(pythonKeywordsL, maybeAdd);
        forEach(pythonKeywordsU, maybeAdd);
    }

    if (context) {
      // If this is a property, see if it belongs to some object we can
      // find in the current environment.
      var obj = context.pop(), base;

      if (obj.type == "variable")
          base = obj.string;
      else if(obj.type == "variable-3")
          base = ":" + obj.string;

      while (base != null && context.length)
        base = base[context.pop().string];
      if (base != null) gatherCompletions(base);
    }
    return found;
  }
})();
