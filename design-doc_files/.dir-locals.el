;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((plantuml-mode . ((eval . (local-lambda-define-local-defun set-debug-on-error nil
			     (interactive)
			     (setq-local debug-on-error t)))
		   (mode . local-lambda))))
