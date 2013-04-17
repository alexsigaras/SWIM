var x = '';
$(function() {
        // Creating the console.
        var header = 'Welcome to the Swim Editor!\n';
        window.jqconsole = $('#console').jqconsole(header, 'Swim> ');

        // Abort prompt on Ctrl+Z.
        jqconsole.RegisterShortcut('Z', function() {
          jqconsole.AbortPrompt();
          handler();
        });
        
        // Move to line start Ctrl+A.
        jqconsole.RegisterShortcut('A', function() {
          jqconsole.MoveToStart();
          handler();
        });
        
        // Move to line end Ctrl+E.
        jqconsole.RegisterShortcut('E', function() {
          jqconsole.MoveToEnd();
          handler();
        });
        
        jqconsole.RegisterMatching('{', '}', 'brace');
        jqconsole.RegisterMatching('(', ')', 'paran');
        jqconsole.RegisterMatching('[', ']', 'bracket');
        // Handle a command.
        var handler = function(command) {
          if (command) {
            try {
              $.ajax({
                url: "code",
                type: "GET",
                async : false,
                data:{token:command},
                dataType:"html",
              }).done(function(html) {
                x = x+ html;
              });

              jqconsole.Write('==> ' + x + '\n');
            } catch (e) {
              jqconsole.Write('ERROR: ' + e.message + '\n');
            }
          }
          jqconsole.Prompt(true, handler, function(command) {
            // Continue line if can't compile the command.
            try {
              Function(command);
            } catch (e) {
              if (/[\[\{\(]$/.test(command)) {
                return 1;
              } else {
                return 0;
              }
            }
            return false;
          });
        };

        // Initiate the first prompt.
        handler();
      });