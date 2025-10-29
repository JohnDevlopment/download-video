;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((python-mode . ((eval . (when (string-match-p "app\\.py\\'" (buffer-file-name))
			   (local-lambda-define-skeleton add-option
			     "Insert an option."
			     "Name: "
			     str ": Annotated[" \n
			     (skeleton-read "Type: ") ?, \n
			     "typer.Option(show_default=False, "
			     "help=\"" (skeleton-read "Help: ") "\")" \n
			     "]" > '(end-of-visual-line) _)
			   (local-lambda-define-skeleton add-argument
			     "Insert an option."
			     "Name: "
			     str ": Annotated[" \n
			     (skeleton-read "Type: ") ?, \n
			     "typer.Argument(show_default=False, "
			     "help=\"" (skeleton-read "Help: ") "\")" \n
			     "]" > '(end-of-visual-line) _))))))
