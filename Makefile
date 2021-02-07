release:
		rm -f ../gopass.alfredworkflow
		zip -r ./gopass.alfredworkflow ./* -x@alfred_package.ignore
