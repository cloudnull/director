# User facing DSL

* TOC
{:toc}

When interacting with the **User** CLI utility executive and orchestration
operations follow a simple DSL inspired by the `Containerfile` specification.

> The AIM of Director isn't to create a new programing language, it is to get
  things done, and then get out of the way.

### Verbs

This is a short list of the available verbs.

##### `RUN`

Syntax: `STRING`

Execute a command. The client terminal will execute using `/bin/sh`.

Extra arguments available to the `RUN` verb.

`--stdout-arg STRING` - Sets the stdout of a given command to defined cached
argument.

##### `ARG`

Syntax: `KEY VALUE`

Sets a cached item within the environment.

##### `ENV`

The same as `ARG`.

##### `ADD`

syntax: `SOURCE DESTINATION`

Copy a file or glob of files to a remote system. This method allows
operators to define multiple files on the CLI using the specific file, or a
glob of files within a given path.

> When copying multiple files, ensure that the destination path ends with an
  operating system separator.

Extra arguments available to the `ADD` verb.

`--chown user[:group]` - Sets the ownership of a recently transferred file to
a defined user and group (optionally).

`--blueprint` - The blueprint option instructs the client to read and render
a copied file. The file will be rendered using cached arguments.

##### `COPY`

The same as `ADD`.

##### `WORKDIR`

Syntax: `STRING`

Create a directory on the client system.

##### `CACHEFILE`

Syntax: `STRING`

Read a **JSON** or **YAML** file on the client side and load the contents into
argument cache. While cached arguments can easily be defined using the `ARG` or
`ENV` verb, the `CACHEFILE` verb provides a way to load thousands of arguments
using a single action.

## Extra options

Every job has the ability to skip a cache hit should one be present on the
client node. To instruct the system to ignore all forms of cache, add the
`--skip-cache` to the job definition.

``` shell
$ director exec --verb RUN '--skip-cache echo -e "hello world"'
```

Every job can also be executed only one time. This is useful when orchestrating
a complex deployment where service setup only needs to be performed once. Use
the `--run-once` flag in your command to ensure it's only executed one time.

``` shell
$ director exec --verb RUN '--run-once echo -e "hello world"'
```