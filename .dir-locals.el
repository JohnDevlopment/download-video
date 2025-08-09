;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((eval . (unless
		     (and
		      (fboundp 'mc-magitupdate)
		      (key-binding
		       (kbd "C-x C-k 2")))
		   (defun mc-magitupdate
		       (&optional arg)
		     "Keyboard macro."
		     (interactive "p")
		     (kmacro-exec-ring-item
		      '("oqog" 0 "%d")
		      arg))
		   (function-put 'mc-magitupdate 'kmacro t)
		   (global-set-key
		    (kbd "C-x C-k 2")
		    #'mc-magitupdate)))
	 (eval . (unless
		     (and
		      (fboundp 'mc-commitdlg)
		      (key-binding
		       (kbd "C-x C-k 1")))
		   (defun mc-commitdlg
		       (&optional arg)
		     "Keyboard macro."
		     (interactive "p")
		     (kmacro-exec-ring-item
		      '([24 111 3 99 99 100 tab tab]
			0 "%d")
		      arg))
		   (function-put 'mc-commitdlg 'kmacro t)
		   (global-set-key
		    (kbd "C-x C-k 1")
		    #'mc-commitdlg)))
	 (org-special-block-add-html-extra . nil)
	 (eval . (unless
		     (fboundp 'mc-foldview)
		   (defun mc-foldview
		       (&optional arg)
		     "Keyboard macro."
		     (interactive "p")
		     (kmacro-exec-ring-item
		      '("fmv" 0 "%d")
		      arg))))))
 (org-mode . ((mode . local-lambda)
	      (eval . (progn
			(local-lambda-define-skeleton name "docstring" "Caption: " "\\begin{figure}[htbp]" n "\\centering" n "\\begin{adjustbox}{max width=\\textwidth, max height="
						      (progn
							(setq v1
							      (read-number "Max height [0,1]: " 0.7))
							(prin1-to-string
							 (min v1 1.0)))
						      "\\textheight, keepaspectratio}" n "\\includegraphics{"
						      (f-relative
						       (read-file-name "Image: "))
						      125 n "\\end{adjustbox}" n "\\caption{" str 125 n "\\end{figure}")))
	      (mode . display-fill-column-indicator)
	      (mode . auto-fill))))
