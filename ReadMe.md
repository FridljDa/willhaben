
## Setup a PostgreSQL docker container for this workshop:
```
cd scripts
docker-compose up -d
```
In Windows, if the connection to the database fails with an authentication error, it might be that the init-user-db.sh is not run automatically upon container creation. The likely root cause is that Windows has converted the file to CRLF line endings (which commonly occurs due to the global git setting `core.autocrlf`), while the docker container needs LF line endings. To fix it, try to reset the file to LF line endings and restart the container.

## Build the projects

Make sure you have a JDK with at least version 17 installed.

In the repository's root folder:
Linux, Mac:
```{bash}
./gradlew clean compileTestJava
```

Windows:
```{PowerShell}
.\gradlew.bat clean compileTestJava

```

## (Optional - for maintainers) Run tests of solution projects

To run quickly run all tests on solutions, e.g. after a dependency update, the following can be helpful:
```
for project in  *solution* ; do ./gradlew ":$project:test" ; done
```

## Visualize the DB schema:
* In IntelliJ: click on the schema and press Ctrl + Alt + Shift + U
* In Eclipse with DBeaver plugin/DBeaver stand-alone: right-click on the schema (e.g. in the Database Navigator or Database Explorer) and select "View Diagram"
* In VS Code with the corresponding plug-in
