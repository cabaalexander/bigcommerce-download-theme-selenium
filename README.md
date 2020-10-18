# bigcommerce download theme automation

## Dependencies

- Have the `.env` file configured before running
- Make sure `make` command is available in the terminal
- `credentials.json` file (google project credentials file)

### .env

```
USER="" # artbead user
PASSWORD="" # artbead password
```

### Usage

```
$ make download
```

Download will open up the browser and prompt you to authenticate the application
to access your GMAIL (this is to read the token sent by bigcommerce) and then
go to the frontstore and start download

Note: The browser cannot be closed until the download finishes (this is the only
task is not automated) after that you should hit the `extract` command

```
$ make extract project_folder="your project directory"
```

This command will search for one "Chiara" compressed file (make sure you only
have one "Chiara" zip in your downloads folder, the one you just recently
downloaded with the command `download`)
