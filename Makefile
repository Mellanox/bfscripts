RPM_BASE:=$(shell \
  rpmspec --query --qf "%{name}-%{version}-%{release}" mlxbf-bfscripts.spec)
SRPM_NAME:=$(RPM_BASE).src.rpm
TAR_BASE:=$(shell \
  rpmspec --query --qf "%{name}-%{version}" mlxbf-bfscripts.spec)
TAR_NAME:=$(TAR_BASE).tar.gz
GIT_FILES:=$(shell git ls-files -co --exclude-standard)

.PHONY: all clean srpm
all:

clean:
	rm -rf RPMBUILD
	rm -rf git_dir_pack
	rm -f mlxbf-bfscripts*.src.rpm

srpm: $(SRPM_NAME)

RPMBUILD/SOURCES/$(TAR_NAME): $(GIT_FILES)
	mkdir -p RPMBUILD/SOURCES
	rm -rf git_dir_pack
	mkdir -p git_dir_pack/$(TAR_BASE)
	rsync --relative $(GIT_FILES) git_dir_pack/$(TAR_BASE)
	(cd git_dir_pack; tar -zcvf ../$@ $(TAR_BASE))

$(SRPM_NAME): RPMBUILD/SOURCES/$(TAR_NAME) mlxbf-bfscripts.spec
	rpmbuild -bs --define "_topdir $(shell pwd)/RPMBUILD" mlxbf-bfscripts.spec
	cp RPMBUILD/SRPMS/$(SRPM_NAME) ./
