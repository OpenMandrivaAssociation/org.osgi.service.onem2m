Name:		org.osgi.service.onem2m
Version:	1.0.0
Release:	1
Summary:	OSGi oneM2M Service Layer API
Group:		Development/Java
License:	ASL 2.0
URL:		https://docs.osgi.org/
Source0:	https://repo1.maven.org/maven2/org/osgi/org.osgi.service.onem2m/%{version}/org.osgi.service.onem2m-%{version}-sources.jar
Source1:	https://raw.githubusercontent.com/osgi/osgi/r8-cmpn-final/LICENSE#/org.osgi.service.onem2m-%{version}-LICENSE

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.osgi:osgi.core)
BuildRequires:	mvn(org.osgi:org.osgi.util.promise)
BuildRequires:	mvn(org.osgi:org.osgi.annotation.versioning)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
OSGi oneM2M Service Layer 1.0.0. ServiceLayer returns Promises from
OSGi Promise 1.3. Resource and request DTOs extend org.osgi.dto.DTO,
which is already inside OSGi Core 6, so this package does not depend
on a separate DTO jar. Both package versions are 1.0. Versioning
annotations are compile-time only. This build targets Java 8.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
rm -rf META-INF
cp -p %{SOURCE1} LICENSE
mkdir -p src/main/java
mv org src/main/java/
python - <<'PY'
from pathlib import Path

root = Path("src/main/java")
names = sorted(str(path.relative_to(root)) for path in root.rglob("*.java"))
expect = [
    "org/osgi/service/onem2m/NotificationListener.java",
    "org/osgi/service/onem2m/OneM2MException.java",
    "org/osgi/service/onem2m/ServiceLayer.java",
    "org/osgi/service/onem2m/dto/AttributeDTO.java",
    "org/osgi/service/onem2m/dto/ChildResourceRefDTO.java",
    "org/osgi/service/onem2m/dto/Constants.java",
    "org/osgi/service/onem2m/dto/DasInfoDTO.java",
    "org/osgi/service/onem2m/dto/FilterCriteriaDTO.java",
    "org/osgi/service/onem2m/dto/GenericDTO.java",
    "org/osgi/service/onem2m/dto/IPEDiscoveryRequestDTO.java",
    "org/osgi/service/onem2m/dto/LocalTokenIdAssignmentDTO.java",
    "org/osgi/service/onem2m/dto/NotificationDTO.java",
    "org/osgi/service/onem2m/dto/NotificationEventDTO.java",
    "org/osgi/service/onem2m/dto/PrimitiveContentDTO.java",
    "org/osgi/service/onem2m/dto/ReleaseVersion.java",
    "org/osgi/service/onem2m/dto/RequestPrimitiveDTO.java",
    "org/osgi/service/onem2m/dto/ResourceDTO.java",
    "org/osgi/service/onem2m/dto/ResourceWrapperDTO.java",
    "org/osgi/service/onem2m/dto/ResponsePrimitiveDTO.java",
    "org/osgi/service/onem2m/dto/ResponseTypeInfoDTO.java",
    "org/osgi/service/onem2m/dto/SecurityInfoDTO.java",
    "org/osgi/service/onem2m/dto/package-info.java",
    "org/osgi/service/onem2m/package-info.java",
]
if names != expect:
    raise SystemExit("java files " + " ".join(names))
for rel in (
    "org/osgi/service/onem2m/package-info.java",
    "org/osgi/service/onem2m/dto/package-info.java",
):
    text = (root / rel).read_text(encoding="utf-8")
    if '@Version("1.0")' not in text:
        raise SystemExit("package version changed " + rel)
    if '@Version("1.0.0")' in text:
        raise SystemExit("package version became 1.0.0 " + rel)
layer = (root / "org/osgi/service/onem2m/ServiceLayer.java").read_text(encoding="utf-8")
if "import org.osgi.util.promise.Promise;" not in layer:
    raise SystemExit("ServiceLayer no longer returns Promises")
if "import org.osgi.dto." in layer:
    raise SystemExit("ServiceLayer started importing DTO directly")
if list(Path(".").rglob("packageinfo")) or list(Path(".").rglob("about.html")):
    raise SystemExit("unexpected packageinfo or about.html")
if "Apache License" not in Path("LICENSE").read_text(encoding="utf-8"):
    raise SystemExit("LICENSE is not the Apache license")
if list(Path(".").rglob("*.jar")) or list(Path(".").rglob("*.class")):
    raise SystemExit("prebuilt binary remains")
for pom in Path(".").rglob("pom.xml"):
    pom.unlink()

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.osgi</groupId>
  <artifactId>org.osgi.service.onem2m</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>org.osgi:org.osgi.service.onem2m</name>
  <description>OSGi oneM2M Service Layer.</description>
  <url>https://docs.osgi.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.core</artifactId>
      <version>6.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.util.promise</artifactId>
      <version>1.3.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.annotation.versioning</artifactId>
      <version>1.1.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>org.osgi.service.onem2m</artifactId>",
    "<artifactId>osgi.core</artifactId>",
    "<version>6.0.0</version>",
    "<artifactId>org.osgi.util.promise</artifactId>",
    "<version>1.3.0</version>",
    "<artifactId>org.osgi.annotation.versioning</artifactId>",
    "<version>1.1.0</version>",
    "<scope>provided</scope>",
    "<version>%{version}</version>",
    "<release>8</release>",
    "</project.build.sourceEncoding>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
if pom.count("<version>1.0.0</version>") != 1:
    raise SystemExit("version 1.0.0 count")
if pom.count("<version>6.0.0</version>") != 1:
    raise SystemExit("core version count")
if pom.count("<version>1.3.0</version>") != 1:
    raise SystemExit("promise version count")
if pom.count("<version>1.1.0</version>") != 1:
    raise SystemExit("versioning count")
if pom.count("<scope>provided</scope>") != 1:
    raise SystemExit("provided scope count")
for needle in (
    "junit",
    "SNAPSHOT",
    "<source>",
    "<target>",
    "<parent>",
    "felix",
    "maven-bundle-plugin",
    "<artifactId>osgi.annotation</artifactId>",
    "<artifactId>org.osgi.dto</artifactId>",
    "<artifactId>org.osgi.util.function</artifactId>",
    "<version>1.0</version>",
    "<version>8.0.1</version>",
    "<version>8.1.0</version>",
    "projectbuild.sourceEncoding",
):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/org.osgi.service.onem2m-%{version}.jar --describe-module org.osgi.service.onem2m > module-describe.txt
grep -q '^org.osgi.service.onem2m' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }
python - <<'PY'
import zipfile
from pathlib import Path
jar = Path("target/org.osgi.service.onem2m-%{version}.jar")
with zipfile.ZipFile(jar) as zf:
    names = set(zf.namelist())
    required = {
        "org/osgi/service/onem2m/NotificationListener.class",
        "org/osgi/service/onem2m/OneM2MException.class",
        "org/osgi/service/onem2m/ServiceLayer.class",
        "org/osgi/service/onem2m/dto/AttributeDTO.class",
        "org/osgi/service/onem2m/dto/ChildResourceRefDTO.class",
        "org/osgi/service/onem2m/dto/Constants.class",
        "org/osgi/service/onem2m/dto/DasInfoDTO.class",
        "org/osgi/service/onem2m/dto/FilterCriteriaDTO$FilterOperation.class",
        "org/osgi/service/onem2m/dto/FilterCriteriaDTO$FilterUsage.class",
        "org/osgi/service/onem2m/dto/FilterCriteriaDTO.class",
        "org/osgi/service/onem2m/dto/GenericDTO.class",
        "org/osgi/service/onem2m/dto/IPEDiscoveryRequestDTO.class",
        "org/osgi/service/onem2m/dto/LocalTokenIdAssignmentDTO.class",
        "org/osgi/service/onem2m/dto/NotificationDTO.class",
        "org/osgi/service/onem2m/dto/NotificationEventDTO$NotificationEventType.class",
        "org/osgi/service/onem2m/dto/NotificationEventDTO.class",
        "org/osgi/service/onem2m/dto/PrimitiveContentDTO.class",
        "org/osgi/service/onem2m/dto/ReleaseVersion.class",
        "org/osgi/service/onem2m/dto/RequestPrimitiveDTO$DesiredIdentifierResultType.class",
        "org/osgi/service/onem2m/dto/RequestPrimitiveDTO$Operation.class",
        "org/osgi/service/onem2m/dto/RequestPrimitiveDTO$ResultContent.class",
        "org/osgi/service/onem2m/dto/RequestPrimitiveDTO.class",
        "org/osgi/service/onem2m/dto/ResourceDTO.class",
        "org/osgi/service/onem2m/dto/ResourceWrapperDTO.class",
        "org/osgi/service/onem2m/dto/ResponsePrimitiveDTO$ContentStatus.class",
        "org/osgi/service/onem2m/dto/ResponsePrimitiveDTO.class",
        "org/osgi/service/onem2m/dto/ResponseTypeInfoDTO$ResponseType.class",
        "org/osgi/service/onem2m/dto/ResponseTypeInfoDTO.class",
        "org/osgi/service/onem2m/dto/SecurityInfoDTO$SecurityInfoType.class",
        "org/osgi/service/onem2m/dto/SecurityInfoDTO.class",
        "org/osgi/service/onem2m/dto/package-info.class",
        "org/osgi/service/onem2m/package-info.class",
    }
    missing = sorted(required - names)
    if missing:
        raise SystemExit("missing " + " ".join(missing))
    extra = sorted(name for name in names if name.endswith(".class") and name not in required)
    if extra:
        raise SystemExit("extra " + " ".join(extra))
    if any(name.endswith("packageinfo") for name in names):
        raise SystemExit("unexpected packageinfo")
    dto_classes = (
        "org/osgi/service/onem2m/dto/AttributeDTO.class",
        "org/osgi/service/onem2m/dto/ChildResourceRefDTO.class",
        "org/osgi/service/onem2m/dto/DasInfoDTO.class",
        "org/osgi/service/onem2m/dto/FilterCriteriaDTO.class",
        "org/osgi/service/onem2m/dto/GenericDTO.class",
        "org/osgi/service/onem2m/dto/IPEDiscoveryRequestDTO.class",
        "org/osgi/service/onem2m/dto/LocalTokenIdAssignmentDTO.class",
        "org/osgi/service/onem2m/dto/NotificationDTO.class",
        "org/osgi/service/onem2m/dto/PrimitiveContentDTO.class",
        "org/osgi/service/onem2m/dto/RequestPrimitiveDTO.class",
        "org/osgi/service/onem2m/dto/ResourceDTO.class",
        "org/osgi/service/onem2m/dto/ResourceWrapperDTO.class",
        "org/osgi/service/onem2m/dto/ResponsePrimitiveDTO.class",
        "org/osgi/service/onem2m/dto/ResponseTypeInfoDTO.class",
        "org/osgi/service/onem2m/dto/SecurityInfoDTO.class",
    )
    for rel in dto_classes:
        if b"org/osgi/dto/DTO" not in zf.read(rel):
            raise SystemExit("DTO superclass missing " + rel)
    layer = zf.read("org/osgi/service/onem2m/ServiceLayer.class")
    if b"org/osgi/util/promise/Promise" not in layer or b"org/osgi/annotation/versioning/ProviderType" not in layer:
        raise SystemExit("ServiceLayer lost Promise or ProviderType")
    if b"org/osgi/util/function/" in layer:
        raise SystemExit("ServiceLayer gained a function reference")
    listener = zf.read("org/osgi/service/onem2m/NotificationListener.class")
    if b"org/osgi/annotation/versioning/ConsumerType" not in listener:
        raise SystemExit("NotificationListener lost ConsumerType")
    for rel in (
        "org/osgi/service/onem2m/package-info.class",
        "org/osgi/service/onem2m/dto/package-info.class",
    ):
        info = zf.read(rel)
        if b"org/osgi/annotation/versioning/Version" not in info or b"1.0" not in info:
            raise SystemExit("package version missing " + rel)
        if b"1.0.0" in info:
            raise SystemExit("package version became 1.0.0 " + rel)
PY

%files -f .mfiles
%doc LICENSE
