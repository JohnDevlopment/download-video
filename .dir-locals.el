;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((eval . (progn
		   (unless (and (fboundp 'mc-commitdlg)
				(key-binding (kbd "C-x C-k 1")))
		     (defun mc-commitdlg (&optional arg)
		       "Keyboard macro."
		       (interactive "p")
		       (kmacro-exec-ring-item '([24 111 3 99 99 100 tab tab] 0 "%d") arg))
		     (function-put 'mc-commitdlg 'kmacro t)
		     (global-set-key (kbd "C-x C-k 1") #'mc-commitdlg))
		   (unless (and (fboundp 'mc-magitupdate)
				(key-binding (kbd "C-x C-k 2")))
		     (defun mc-magitupdate (&optional arg)
		       "Keyboard macro."
		       (interactive "p")
		       (kmacro-exec-ring-item '("oqog" 0 "%d") arg))
		     (function-put 'mc-magitupdate 'kmacro t)
		     (global-set-key (kbd "C-x C-k 2") #'mc-magitupdate))
		   (unless (and (fboundp 'mc-magitupdate2)
				(key-binding (kbd "C-x C-k 3")))
		     (defun mc-magitupdate2 (&optional arg)
		       "Keyboard macro."
		       (interactive "p")
		       (kmacro-exec-ring-item '("goq" 0 "%d") arg))
		     (global-set-key (kbd "C-x C-k 3") #'mc-magitupdate2))))
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
 (python-mode . ((mode . visual-line)))
 (magit-mode . ((mode . local-lambda)
		(eval . (progn
			  (local-lambda-define-local-defun commit-add-file nil
			    (interactive)
			    (if
				(cl-ext-progn
				  (move-beginning-of-line nil)
				  (looking-at "\\(deleted\\|modified\\|new file\\)[ \t]+\\(.+\\)"))
				(let*
				    ((tag
				      (pcase
					  (match-string-no-properties 1)
					("modified" "update")
					("new file" "add")
					("deleted" "remove")))
				     (file
				      (match-string-no-properties 2)))
				  (call-interactively #'magit-commit-create)
				  (run-with-idle-timer 1 nil #'insert
						       (format "%s %s" tag file)))))))))
 (org-mode . ((mode . local-lambda)
	      (mode . visual-line)
	      (eval . (progn
			(unless (fboundp 'commit-ddoc)
			  (defun commit-ddoc ()
			    (interactive)
			    (let ((path (org-get-outline-path t t)))
			      (with-temp-buffer
				(insert (s-join "/" (cons "design doc" path)))
				(kill-region (point-min) (point-max))))))))
	      (eval . (progn
			(local-lambda-define-skeleton name
			  "docstring"
			  "Caption: "
			  "\\begin{figure}[htbp]" \n
			  "\\centering" \n
			  "\\begin{adjustbox}{max width=\\textwidth, max height="
			  (progn
			    (setq v1
				  (read-number "Max height [0,1]: " 0.7))
			    (prin1-to-string
			     (min v1 1.0)))
			  "\\textheight, keepaspectratio}" n "\\includegraphics{"
			  (f-relative
			   (read-file-name "Image: "))
			  125 n "\\end{adjustbox}" n "\\caption{" str 125 n "\\end{figure}"))))))
