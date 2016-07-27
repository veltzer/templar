<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>${tdefs.project_name}</title>
		<link rel="shortcut icon" href="../static/favicon.ico"/>
		<meta name="Description" content="${tdefs.project_long_description}"/>
		<meta name="Keywords" content="${tdefs.personal_fullname}, ${tdefs.personal_slug}, ${tdefs.project_name}, ${', '.join(tdefs.project_keywords)}"/>
		${tdefs.project_google_analytics_snipplet}
	</head>
	<body>
		<h1>Welcome to the <i>${tdefs.project_name}</i> web site</h1>
		
		<p>current version is ${tdefs.git_lasttag}</p>

		<p>
		<b>${tdefs.project_name}</b> is a templating system for building projects in any language.
		The idea is that when writing a project you want to compile files (javascript, python, html, etc)
		from various bits and pieces of information which you have in all kinds of files.
		<b>${tdefs.project_name}</b> will let you do that easily and combine this process into your build system.
		</p>
		<p>
			I would appreciate donations so that I could use my time to work on <b>${tdefs.project_name}</b> more.
			If you do donate and would like me to work on some specific features then be sure to mention them
			in your donation remark on paypal.
		</p>
		${tdefs.project_paypal_donate_button_snipplet}
		<p>
			Copyright ${tdefs.personal_fullname}, ${tdefs.project_copyright_years}
			<a href="mailto:${tdefs.personal_email}">${tdefs.personal_email}</a>
		</p>
	</body>
</html>
