# Gopass-Alfred

Workflow to interact with gopass from [Alfred 3](https://www.alfredapp.com/workflows/) on MacOS. 
You will need an Alfred 3 license in order to use workflows. 
Currently querying entries and copying username or password to clipboard is supported.

## Screenshot

![gopass alfred screenshot](./screenshot.png)

## Installation

Download the [latest release package](https://github.com/gopasspw/gopass-alfred/releases/latest) from github or build your own via `make release` in checked out repository.

## Autotyping

The plugin can also type a username / password combination automatically. You can start the action by issuing `gpa` in Alfred.

By default, a field called `autotype` will be used. The value can contain various statements.

Example: `user :tab :pass`

### Trigger Options

However, there are more options:

| Option        | Effect                                                                        |
|---------------|-------------------------------------------------------------------------------|
| user / pass   | A field name (not prefixed with `:`. Can reference any other available field. |
| `:tab`        | Issues a tab key                                                              |
| `:enter`      | Enter key                                                                     |
| `:space`      | Space key                                                                     |
| `:delete`     | Delete key                                                                    |
| `:delay`      | Waits one second before continuing                                            |
| `:clearField` | Clears the current input field (Issues Ctrl+A + backspace)                    |

A rather typical example looks like the following:

```
myPassword
---
autotype: :clearField user :tab pass :tab :tab :enter :delay :someYk :enter
user: myUsername
usernamePassword: user :tab pass
```

### Custom autotype options

You might have noted `:someYk` as option which was not listed in the table above. Not all commands can be hardcoded in a table like the one above. For example, you might have a form that requires a one-time-password such as from a YubiKey. You might be able to retrieve the information from a `bash` command - however.

Those commands can be put to a `.gopass_autotype_handlers.json` json file. It can be place in `$XDG_CONFIG`, which defaults to your `HOME` directory. Example: `/users/someUser/.gopass_autotype_handlers.json`

An example file content looks like the following:

```json
{
  ":someYk": "/usr/local/bin/ykman oath code | grep \"YubiKey:name\" | sed 's/.*\\([0-9]\\{6\\}\\)$/\\1/g'"
}
```

This example will retrieve a current TOTP token from the YubiKey by asking `ykman` for the current value and converts the output to the token.

### Autotyping other fields than `autotype`

The `gpa` command will always run the `autotype` field. However, you can also use `gpf` to autotype any available field in the gopass file. This also includes the trigger options from the table above.

## Development

Contributions to this project are welcome!
