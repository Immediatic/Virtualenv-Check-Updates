#!/usr/bin/env python

try:
	import commands
except:
	print "Unable to import commands"
	exit(1)
	
try:
	import pip
except:
	print "Unable to import pip, are you in the virtualenv?"
	exit(1)

try:
	import xmlrpclib
except:
	print "Unable to import xmlrpclib"
	exit(1)

class Package(object):
    name = "n/d"
    version = "0.0"

def checkPackageVersion(packageName, currentVersion=None):
    server = xmlrpclib.Server('http://pypi.python.org/pypi')
    versionsAvailable = server.package_releases(packageName)

    maxLength = 30
    extendedPackagename = packageName[0:maxLength]
    if len(extendedPackagename) < maxLength:
        for i in range(maxLength - len(extendedPackagename)):
            extendedPackagename += " "
    
    if currentVersion:
        res = "%s\t%s\t\t%s\t\t" % (extendedPackagename, currentVersion, versionsAvailable[0])
    else:
        res = "%s\t\t\t%s\t\t" % (extendedPackagename, versionsAvailable[0])

    if currentVersion != versionsAvailable[0]:
        res += "\tNEW"
        print res
        return True
    else:
        print res
        return False

def readPipRequirements():
    packages = []

    requirements = commands.getoutput("pip freeze")

    for requirement in requirements.split("\n"):
        if len(requirement) == 0 or requirement[0] == "#":
            continue

        p = Package()

        splitted = requirement.split("==")
        if len(splitted) == 2:
            p.name = splitted[0]
            p.version = splitted[1]
            packages.append(p)

    return packages

if __name__ == "__main__":
    print "Package name\t\t\tCurrent Version\tAvailable version"
    print "============\t\t\t===============\t================="

    packages = readPipRequirements()
    
    for package in packages:
        checkPackageVersion(package.name, package.version)