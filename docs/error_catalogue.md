# Error catalogue: crf-batches-01-02

- Split: dev of `splits/pool-v1.json`
- Gold origin: model_draft_accepted 172. Records not labelled by hand measure agreement with the drafting model: a disagreement with them is not necessarily an error
- Predictions: `reports/agreement/predictions/crf-batches-01-02.jsonl`
- Documents: 172; disagreements: 432

Spans are marked «like this» in their sentence. Excerpts are advisory text from the GitHub Advisory Database (CC BY 4.0).

| Error type | Count | Proposed remedy |
|---|---:|---|
| reversed_meaning | 9 | Add a minimal pair for this cue to the challenge set; check the role rule (guidelines §5) and add training examples with the opposite polarity. |
| invented_prerequisite | 59 | Add hard negatives of this kind (impact, mechanism, workaround, background mention) to training; consider a stricter accept threshold. |
| missed_condition | 265 | Check whether the wording is covered by any cue or feature; target it with uncertainty sampling. |
| boundary_error | 50 | Clarify the span-boundary rule (guidelines §6) with this example; check tokenisation of the identifiers involved. |
| category_error | 13 | Add this case to the category tie-breakers (guidelines §4). |
| role_error | 7 | Add this case to the role table (guidelines §5). |
| group_error | 16 | Check the lead-in / connective that sets the logic; add list examples. |
| spurious_condition | 13 | Check why a non-requirement was predicted here; add hard negatives. |

## reversed_meaning (9)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-4xfr-4p46-gc6p | A staff user holding the global add permission for a plugin type, but with «no access to a given placeholder/page», can copy that placeholder's plugins into their own clipboard and read content (e.g. link names/URLs, te… | ACCESS/NOT_REQUIRED "access to a given placeholder/page" | ACCESS/REQUIRED "no access to a given placeholder/page" |
| GHSA-4xfr-4p46-gc6p | Requires «CMS_PERMISSION=True with per-placeholder/page restrictions». | CONFIGURATION/REQUIRED "CMS_PERMISSION=True with per-placeholder/page restrictions" | CONFIGURATION/NOT_REQUIRED "CMS_PERMISSION=True" |
| GHSA-53q9-r3pm-6pq6 | When «loading model using torch.load with weights_only=True», it can still achieve RCE. | CONFIGURATION/NOT_REQUIRED "weights_only=True" | CONFIGURATION/REQUIRED "loading model using torch.load with weights_only=True" |
| GHSA-6qv9-48xg-fc7f | Most applications either «do not use templates or else use hardcoded templates» and are not vulnerable. | USAGE/EXCEPTION "do not use templates or else use hardcoded templates" | USAGE/REQUIRED "do not use templates or else use hardcoded templates" |
| GHSA-6qv9-48xg-fc7f | Most applications either «do not use templates or else use hardcoded templates» and are not vulnerable. | USAGE/EXCEPTION "do not use templates or else use hardcoded templates" | USAGE/REQUIRED "do not use templates or else use hardcoded templates" |
| GHSA-75mc-3pjc-727q | It was reported by @kircheneer that in the default implementation used in Nautobot, as provided by django-db-file-storage, these URLs do not by default require any «user authentication to access»; they should instead be… | ACCESS/NOT_REQUIRED "user authentication" | ACCESS/REQUIRED "user authentication to access" |
| GHSA-mxh2-ccgj-8635 | This allows access to web_server functionality (including OTA, if enabled) without knowing any «information about the correct username or password». | ACCESS/NOT_REQUIRED "information about the correct username or password" | ACCESS/REQUIRED "correct username or password" |
| GHSA-qccp-gfcp-xxvc | When «following cross-origin redirects for requests made using urllib3’s high-level APIs, such as urllib3.request(), PoolManager.request(), and ProxyManager.request()», sensitive headers — Authorization, Cookie, and Pro… | USAGE/EXCEPTION "high-level APIs, such as urllib3.request(), PoolManager.request(), and ProxyManager.request()" | USAGE/REQUIRED "following cross-origin redirects for requests made using urllib3’s high-level APIs" |
| GHSA-qccp-gfcp-xxvc | However, «cross-origin redirects followed from the low-level API via ProxyManager.connection_from_url().urlopen(..., assert_same_host=False)» still forward these sensitive headers. | USAGE/REQUIRED "cross-origin redirects followed from the low-level API via ProxyManager.connection_from_url().urlopen(..., assert_same_host=False)" | CONFIGURATION/NOT_REQUIRED "assert_same_host=False" |

## invented_prerequisite (59)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-23fx-92m6-4f2g | pretalx allows path traversal in «HTML export» | - | USAGE/REQUIRED "HTML export" |
| GHSA-2655-q453-22f9 | The django.http.HttpRequest.get_host function in Django 1.3.x before 1.3.4 and 1.4.x before 1.4.2 allows remote attackers to generate and display arbitrary URLs via «crafted username and password» Host header values. | - | USAGE/REQUIRED "crafted username and password" |
| GHSA-56v6-2fhr-wxgq | Because the payload runs in the «victim's authenticated session», it can lead to actions performed as the victim, session/token theft, and further privilege escalation. | - | USAGE/REQUIRED "victim's authenticated session" |
| GHSA-5p9j-w2wx-qx4c | In the /user/login endpoint, it doesn't check the value of the next parameter when the user is logged in and «passes it directly to redirect which result to open redirect». | - | USAGE/REQUIRED "passes it directly to redirect which result to open redirect" |
| GHSA-64x4-9hc6-r2h6 | The library is not vulnerable to the equivalent of CVE-2020-8912, but only because it currently only «supports AES-CBC as encryption mode». | - | CONFIGURATION/REQUIRED "supports AES-CBC as encryption mode" |
| GHSA-64x4-9hc6-r2h6 | In the current version of the Azure Blob Storage crypto SDK, the only algorithm option that allows users to encrypt files is to AES-CBC, without «computing a MAC on the data». | - | ACCESS/REQUIRED "computing a MAC on the data" |
| GHSA-6p5q-h963-pwwf | The fix is to update to the latest Golang and Python drivers in addition to the latest version of «AGE that is used for PostgreSQL 11 or PostgreSQL 12». | - | USAGE/REQUIRED "AGE that is used for PostgreSQL 11 or PostgreSQL 12" |
| GHSA-6qv9-48xg-fc7f | LangChain Vulnerable to Template Injection via «Attribute Access in Prompt Templates» | - | USAGE/REQUIRED "Attribute Access in Prompt Templates" |
| GHSA-6qv9-48xg-fc7f | A template injection vulnerability exists in LangChain's «prompt template system that allows attackers to access Python object internals through template syntax». | - | USAGE/REQUIRED "prompt template system that allows attackers to access Python object internals through template syntax" |
| GHSA-6qv9-48xg-fc7f | When «template variables» are simple strings (the common case), the impact is limited. | - | USAGE/REQUIRED "template variables" |
| GHSA-6qv9-48xg-fc7f | F-string templates: The implementation used Python's string.Formatter().parse() to «extract variable names from template strings». | - | USAGE/REQUIRED "extract variable names from template strings" |
| GHSA-6qv9-48xg-fc7f | While «f-string templates do not support method calls with ()», they do support [] indexing, which could allow traversal through dictionaries like __globals__ to reach sensitive objects. | - | USAGE/REQUIRED "f-string templates do not support method calls with ()" |
| GHSA-6qv9-48xg-fc7f | The safest approach is to only use Jinja2 templates when you «control the template source». | - | ACCESS/REQUIRED "control the template source" |
| GHSA-6qv9-48xg-fc7f | A template injection vulnerability exists in LangChain's «prompt template system that allows attackers to access Python object internals through template syntax». | - | USAGE/REQUIRED "prompt template system that allows attackers to access Python object internals through template syntax" |
| GHSA-6qv9-48xg-fc7f | When «template variables» are simple strings (the common case), the impact is limited. | - | USAGE/REQUIRED "template variables" |
| … | 44 more | | |

## missed_condition (265)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-23fx-92m6-4f2g | «Organizers» can trigger the overwriting (with the standard pretalx 404 page content) of an arbitrary file. | ACCESS/REQUIRED "Organizers" | - |
| GHSA-2655-q453-22f9 | The «django.http.HttpRequest.get_host function» in Django 1.3.x before 1.3.4 and 1.4.x before 1.4.2 allows remote attackers to generate and display arbitrary URLs via crafted username and password Host header values. | USAGE/REQUIRED "django.http.HttpRequest.get_host function" | - |
| GHSA-27mf-ghqm-j3j8 | aiohttp has a memory leak when «middleware is enabled» when requesting a resource with a non-allowed method | USAGE/REQUIRED "middleware is enabled" | - |
| GHSA-27mf-ghqm-j3j8 | A memory leak can occur when a «request produces a MatchInfoError». | USAGE/REQUIRED "request produces a MatchInfoError" | - |
| GHSA-27mf-ghqm-j3j8 | If the user is «making use of any middlewares with aiohttp.web» then it is advisable to upgrade immediately. | USAGE/REQUIRED "making use of any middlewares with aiohttp.web" | - |
| GHSA-27mf-ghqm-j3j8 | An attacker may be able to exhaust the memory resources of a server by «sending a substantial number (100,000s to millions) of such requests». | ACCESS/REQUIRED "sending a substantial number (100,000s to millions) of such requests" | - |
| GHSA-27x4-j476-jp5f | «easy_install» in setuptools before 0.7 uses HTTP to retrieve packages from the PyPI repository, and does not perform integrity checks on package contents, which allows man-in-the-middle attackers to execute arbitrary c… | USAGE/REQUIRED "easy_install" | - |
| GHSA-2hvc-hwg3-hpvw | Out-of-bounds read in «gather_tree» in PaddlePaddle before 2.4. | USAGE/REQUIRED "gather_tree" | - |
| GHSA-2hwx-mjrm-v3g8 | A «malicious homeserver» could redirect requests to their .well-known file to a large file. | ACCESS/REQUIRED "malicious homeserver" | - |
| GHSA-2j23-fwqm-mgwr | Any «user with a role on a project» is able to list any credentials with the /v3/credentials API when enforce_scope is false. | ACCESS/REQUIRED "user with a role on a project" | - |
| GHSA-2j23-fwqm-mgwr | Any user with a role on a project is able to list any credentials with the /v3/credentials API when «enforce_scope is false». | CONFIGURATION/REQUIRED "enforce_scope is false" | - |
| GHSA-2j23-fwqm-mgwr | «Users with a role on a project» are able to view any other users' credentials, which could (for example) leak sign-on information for Time-based One Time Passwords (TOTP). | ACCESS/REQUIRED "Users with a role on a project" | - |
| GHSA-2m34-jcjv-45xf | Query parameters generated by the «Django admin ForeignKeyRawIdWidget» were not properly URL encoded, leading to a possibility of an XSS attack. | USAGE/REQUIRED "Django admin ForeignKeyRawIdWidget" | - |
| GHSA-2p9h-ccw7-33gf | An exponential ReDoS (Regular Expression Denial of Service) can be triggered in the cleo PyPI package, when an attacker is able to «supply arbitrary input to the Table.set_rows method». | ACCESS/REQUIRED "supply arbitrary input to the Table.set_rows method" | - |
| GHSA-2xwp-m7mq-7q3r | In the affected versions, the AWS Encryption CLI operated in "discovery mode" even when «"strict mode" was specified». | CONFIGURATION/REQUIRED ""strict mode" was specified" | - |
| … | 250 more | | |

## boundary_error (50)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-23fx-92m6-4f2g | pretalx 2.3.1 before 2.3.2 allows path traversal in «HTML export (a non-default feature»). | USAGE/REQUIRED "HTML export" | USAGE/REQUIRED "HTML export (a non-default feature" |
| GHSA-27mf-ghqm-j3j8 | aiohttp has a memory leak when middleware is enabled when «requesting a resource with a non-allowed method» | ACCESS/REQUIRED "requesting a resource with a non-allowed method" | USAGE/REQUIRED "non-allowed method" |
| GHSA-2hwx-mjrm-v3g8 | This affects any server which «accepts federation requests from untrusted servers». | USAGE/REQUIRED "accepts federation requests from untrusted servers" | USAGE/REQUIRED "federation requests from untrusted servers" |
| GHSA-35p3-6j45-prwm | The issue arises when a «large number of tracked metrics are retrieved simultaneously from the Aim web API», causing the web server to become unresponsive. | USAGE/REQUIRED "large number of tracked metrics are retrieved simultaneously from the Aim web API" | USAGE/REQUIRED "Aim web API" |
| GHSA-444r-2whx-3685 | Attackers can «submit crafted POST requests to the admin audit log endpoint with base64-encoded compressed pickle payloads» in the data field to achieve code execution with application privileges. | ACCESS/REQUIRED "submit crafted POST requests to the admin audit log endpoint" | ACCESS/REQUIRED "submit crafted POST requests to the admin audit log endpoint with base64-encoded compressed pickle payloads" |
| GHSA-55x5-fj6c-h6m8 | The «HTML Cleaner in lxml.html lets certain crafted script content pass through, as well as script content in SVG files embedded using data URIs». | USAGE/REQUIRED "HTML Cleaner in lxml.html" | USAGE/REQUIRED "lxml.html lets certain crafted script content pass through, as well as script content in SVG files embedded using data URIs" |
| GHSA-5789-5fc7-67v3 | It is possible for an «authenticated user to access content outside the server's root_dir in siblings directories sharing the same prefix as the root_dir». | PLATFORM/REQUIRED "siblings directories sharing the same prefix as the root_dir" | ACCESS/REQUIRED "authenticated user to access content outside the server's root_dir in siblings directories sharing the same prefix as the root_dir" |
| GHSA-5789-5fc7-67v3 | This can have a tangible impact for «deployments using predictable naming scheme with multi-tenant server», for example user1, user2, user3, ..., user10 etc, as user1 could access and modify files of all user10 - user19… | PLATFORM/UNCERTAIN "deployments using predictable naming scheme with multi-tenant server" | USAGE/REQUIRED "using predictable naming scheme with multi-tenant server" |
| GHSA-64x4-9hc6-r2h6 | The attack requires write access to the container in question, and that the attacker has «access to an endpoint that reveals decryption failures (without revealing the plaintext)» and that when encrypting the CBC option… | ACCESS/REQUIRED "access to an endpoint that reveals decryption failures (without revealing the plaintext)" | ACCESS/REQUIRED "access to an endpoint" |
| GHSA-64x4-9hc6-r2h6 | The attack requires write access to the container in question, and that the attacker has access to an endpoint that reveals decryption failures (without revealing the plaintext) and that when «encrypting the CBC option … | CONFIGURATION/REQUIRED "CBC option was chosen as content cipher" | USAGE/REQUIRED "encrypting the CBC option was chosen as content cipher" |
| GHSA-6966-vjj6-99xv | if «running 4.5.2 or newer, useSystemClipboardForCells is enabled» - it is off by default in 4.5.2+, and always enabled on 4.5.0 and 4.5.1 with no opt-out | CONFIGURATION/REQUIRED "useSystemClipboardForCells is enabled" | CONFIGURATION/UNCERTAIN "running 4.5.2 or newer, useSystemClipboardForCells is enabled" |
| GHSA-6966-vjj6-99xv | Both need «you to click or press a key on that page first». | ACCESS/REQUIRED "click or press a key on that page first" | ACCESS/REQUIRED "you to click or press a key" |
| GHSA-6cjm-4pxw-7xp9 | An «attacker with access to the log data» could use these leaked credentials to login to the Sentry system as superuser. | ACCESS/REQUIRED "attacker with access to the log data" | ACCESS/REQUIRED "access to the log data" |
| GHSA-6qv9-48xg-fc7f | This vulnerability affects applications that «accept untrusted template strings (not just template variables) in ChatPromptTemplate and related prompt template classes». | USAGE/REQUIRED "accept untrusted template strings (not just template variables) in ChatPromptTemplate and related prompt template classes" | USAGE/REQUIRED "accept untrusted template strings" |
| GHSA-6qv9-48xg-fc7f | This vulnerability affects applications that «accept untrusted template strings (not just template variables) in ChatPromptTemplate and related prompt template classes». | USAGE/REQUIRED "accept untrusted template strings (not just template variables) in ChatPromptTemplate and related prompt template classes" | USAGE/REQUIRED "ChatPromptTemplate and related prompt template classes" |
| … | 35 more | | |

## category_error (13)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-33fm-6gp7-4p47 | The SSH management console did not validate the passed input while «adding the SSH host key», which could lead to an argument injection to ssh-add. | USAGE/REQUIRED "adding the SSH host key" | ACCESS/REQUIRED "adding the SSH host key" |
| GHSA-6xcx-gx7r-rccj | In the /license/ endpoint, the detailed view key is not properly validated and sanitized, which can result in a potential cross-site scripting (XSS) vulnerability when «attempting to access a detailed license view that … | ACCESS/REQUIRED "attempting to access a detailed license view that does not exist" | USAGE/REQUIRED "attempting to access a detailed license view that does not exist" |
| GHSA-8mpj-m6qm-5qr8 | Preconditions: application «uses mistune with the Include directive enabled» and renders user-supplied markdown that can reference other user-uploaded files. | USAGE/REQUIRED "uses mistune with the Include directive enabled" | CONFIGURATION/REQUIRED "uses mistune with the Include directive enabled" |
| GHSA-924m-4pmx-c67h | pysaml2 version 4.4.0 and older accept any password when «run with python optimizations enabled». | PLATFORM/REQUIRED "run with python optimizations enabled" | CONFIGURATION/REQUIRED "run with python optimizations enabled" |
| GHSA-9w2p-rh8c-v9g5 | The user «runs an application containing either matplotlib or win32com». | USAGE/REQUIRED "runs an application containing either matplotlib or win32com" | ACCESS/REQUIRED "runs an application containing either matplotlib or win32com" |
| GHSA-c36r-g737-9qp8 | The volume_utils._parse_volume_info function in OpenStack Compute (Nova) before 2015.1.3 (kilo) and 12.0.x before 12.0.1 (liberty) includes the connection_info dictionary in the StorageError message when «using the Xen … | CONFIGURATION/REQUIRED "using the Xen backend" | USAGE/REQUIRED "using the Xen backend" |
| GHSA-crhm-qpjc-cm64 | The cookie parsing code in Django before 1.8.15 and 1.9.x before 1.9.10, when «used on a site with Google Analytics», allows remote attackers to bypass an intended CSRF protection mechanism by setting arbitrary cookies. | PLATFORM/REQUIRED "used on a site with Google Analytics" | USAGE/REQUIRED "used on a site with Google Analytics" |
| GHSA-f4xh-w4cj-qxq8 | Anyone «reachable by HTTP» can trigger the file read. | ACCESS/REQUIRED "reachable by HTTP" | PLATFORM/REQUIRED "reachable by HTTP" |
| GHSA-fgmc-2hqj-86v4 | Vantage6 currently provides an «initial user with username root and password root». | CONFIGURATION/REQUIRED "initial user with username root and password root" | ACCESS/REQUIRED "initial user with username root and password root" |
| GHSA-gj55-2xf9-67rq | The vulnerability depends on «user interaction by opening a malicious notebook with Markdown cells, or Markdown file using JupyterLab preview feature». | ACCESS/REQUIRED "user interaction by opening a malicious notebook with Markdown cells, or Markdown file using JupyterLab preview feature" | USAGE/REQUIRED "user interaction by opening a malicious notebook with Markdown cells, or Markdown file using JupyterLab preview feature" |
| GHSA-h6h9-pphv-m266 | This attack appear to be exploitable via The victim must «open a todo.txt with at least one specially crafted line». | ACCESS/REQUIRED "open a todo.txt with at least one specially crafted line" | USAGE/REQUIRED "open a todo.txt with at least one specially crafted line" |
| GHSA-hxmp-pqch-c8mm | A «malicious or poorly-implemented homeserver» can inject malformed events into a room by specifying a different room id in the path of a /send_join, /send_leave, /invite or /exchange_third_party_invite request. | ACCESS/REQUIRED "malicious or poorly-implemented homeserver" | USAGE/REQUIRED "malicious or poorly-implemented homeserver" |
| GHSA-jwhx-xcg6-8xhj | Servers with static routes that contain compressed variants as symbolic links, pointing outside the root directory, or that «permit users to upload or create such links», are impacted. | USAGE/REQUIRED "permit users to upload or create such links" | ACCESS/REQUIRED "permit users to upload or create such links" |

## role_error (7)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-53q9-r3pm-6pq6 | But now, I just proved that even if you use «weights_only=True», it can still achieve RCE. | CONFIGURATION/NOT_REQUIRED "weights_only=True" | CONFIGURATION/UNCERTAIN "weights_only=True" |
| GHSA-6qv9-48xg-fc7f | However, when «using MessagesPlaceholder with chat message objects», attackers can traverse through object attributes and dictionary lookups (e.g., __globals__) to reach sensitive data such as environment variables. | USAGE/UNCERTAIN "using MessagesPlaceholder with chat message objects" | USAGE/REQUIRED "using MessagesPlaceholder with chat message objects" |
| GHSA-6qv9-48xg-fc7f | However, when «using MessagesPlaceholder with chat message objects», attackers can traverse through object attributes and dictionary lookups (e.g., __globals__) to reach sensitive data such as environment variables. | USAGE/UNCERTAIN "using MessagesPlaceholder with chat message objects" | USAGE/REQUIRED "using MessagesPlaceholder with chat message objects" |
| GHSA-75mc-3pjc-727q | Note that no URL mechanism is provided for listing or traversal of the available file name values, so in practice an unauthenticated user would have to guess names to discover arbitrary files for download, but if a user… | ACCESS/REQUIRED "knows the file name/path value" | ACCESS/UNCERTAIN "knows the file name/path value" |
| GHSA-95px-34x5-p37h | When the «host is controlled by the attacker and uses DNS rebinding», the validation lookup can resolve to a public IP while the later HTTP client lookup resolves to an internal address, allowing SSRF to internal servic… | ACCESS/UNCERTAIN "host is controlled by the attacker and uses DNS rebinding" | ACCESS/REQUIRED "host is controlled by the attacker and uses DNS rebinding" |
| GHSA-f4xh-w4cj-qxq8 | Depending on how the distributed trace system is deployed, triggering a read may not require «authentication». | ACCESS/UNCERTAIN "authentication" | ACCESS/NOT_REQUIRED "authentication" |
| GHSA-rwmf-w63j-p7gv | A «specially crafted SVG file that loads an external resource from a URL». | USAGE/UNCERTAIN "specially crafted SVG file that loads an external resource from a URL" | USAGE/REQUIRED "specially crafted SVG file that loads an external resource from a URL" |

## group_error (16)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-64x4-9hc6-r2h6 | The attack requires «write access to the container in question, and that the attacker has access to an endpoint that reveals decryption failures (without revealing the plaintext) and that when encrypting the CBC option … | ALL of 3 | no group |
| GHSA-64x4-9hc6-r2h6 | This exposes a padding oracle vulnerability: If the attacker has «write access to the blob container bucket and can observe whether or not an endpoint with access to the key can decrypt a file» (without observing the fi… | ALL of 2 | no group |
| GHSA-64x4-9hc6-r2h6 | The attack requires «write access to the container in question, and that the attacker has access to an endpoint» that reveals decryption failures (without revealing the plaintext) and that when encrypting the CBC option… | no group | ALL of 2 |
| GHSA-6966-vjj6-99xv | if running 4.5.2 or newer, «useSystemClipboardForCells is enabled - it is off by default in 4.5.2+, and always enabled on 4.5.0 and 4.5.1 with no opt-out they run a Paste Cells command (e.g. from context menu, command p… | ALL of 3 | no group |
| GHSA-772j-xvf9-qpf5 | A race condition flaw was found in ansible-runner, where an attacker could «watch for rapid creation and deletion of a temporary directory, substitute their directory at that name», and then have access to ansible-runne… | ALL of 2 | no group |
| GHSA-856c-92hv-3vxx | If an «operator-configured destination is later compromised (service takeover, malicious update), or an attacker holds a MITM position on an unprotected network path», that destination can return a 302 Location: to an a… | ANY of 2 | no group |
| GHSA-856c-92hv-3vxx | Attack requires the «operator-configured destination to be compromised or an attacker to be on the network path». | ANY of 2 | no group |
| GHSA-856c-92hv-3vxx | If an «operator-configured destination is later compromised (service takeover, malicious update), or an attacker holds a MITM position on an unprotected network path, that destination can return a 302 Location: to an ar… | no group | ALL of 2 |
| GHSA-8mpj-m6qm-5qr8 | Preconditions: application «uses mistune with the Include directive enabled and renders user-supplied markdown that can reference other user-uploaded files». | ALL of 2 | no group |
| GHSA-97x9-59rv-q5pm | When «verifying W3C Format Verifiable Credentials using JSON-LD with Linked Data Proofs (LDP-VCs)», the result of verifying the presentation document.proof was not factored into the final verified value (true/false) on … | no group | ALL of 2 |
| GHSA-9w2p-rh8c-v9g5 | The user «runs an application containing either matplotlib or win32com. The application is ran as administrator (or at least a user with higher privileges than the attacker). The user's temporary directory is not locked… | UNRESOLVED of 5 | no group |
| GHSA-f4xh-w4cj-qxq8 | The net effect is a trust-boundary crossing: a party with «workspace trace-read access (for example a low-privilege workspace member, a contractor, or a compromised teammate account) gains the ability to read files from… | no group | UNRESOLVED of 2 |
| GHSA-hvq6-2r72-p2x7 | If an «editor could store HTML in data used by a plugin's get_short_description() (or in other values interpolated into the exception message), and that plugin later raised during edit-mode rendering», the payload was p… | ALL of 2 | no group |
| GHSA-jwhx-xcg6-8xhj | Servers with «static routes that contain compressed variants as symbolic links, pointing outside the root directory, or that permit users to upload or create such links», are impacted. | ANY of 2 | no group |
| GHSA-r562-m862-63w3 | This vulnerability affects users that have «set up the agent via the attacher cli 3, the attach API 2, as well as users that have enabled the profiling_inferred_spans_enabled option» | ANY of 2 | no group |
| … | 1 more | | |

## spurious_condition (13)

| Advisory | Excerpt | Gold | Predicted |
|---|---|---|---|
| GHSA-3g2f-4rjg-9385 | The screenshot images were served directly by the HTTP server without «proper access control». | - | ACCESS/NOT_REQUIRED "proper access control" |
| GHSA-4xfr-4p46-gc6p | A staff user can copy plugins out of a placeholder they have no «permission on into their clipboard», then read the (secret) content. | - | ACCESS/NOT_REQUIRED "permission on into their clipboard" |
| GHSA-6qv9-48xg-fc7f | Important Reminder: Many applications do not need «prompt templates». | - | ACCESS/NOT_REQUIRED "prompt templates" |
| GHSA-6qv9-48xg-fc7f | Consider if you need templates at all - Many applications can «work directly with message objects» (HumanMessage, AIMessage, etc.) without templates## Context | - | USAGE/UNCERTAIN "work directly with message objects" |
| GHSA-6qv9-48xg-fc7f | Important Reminder: Many applications do not need «prompt templates». | - | ACCESS/NOT_REQUIRED "prompt templates" |
| GHSA-6qv9-48xg-fc7f | Consider if you need templates at all - Many applications can «work directly with message objects» (HumanMessage, AIMessage, etc.) without templates | - | USAGE/UNCERTAIN "work directly with message objects" |
| GHSA-f5x6-7qgp-jhf3 | in this case, the immutable PERMIT_TYPEHASH is loaded into ecrecover's output buffer right before ecrecover(), and so the output of ecrecover() here when the signature is invalid will be the value of PERMIT_TYPEHASH. in… | - | ACCESS/NOT_REQUIRED "valid address" |
| GHSA-fxq4-r6mr-9x64 | Since GETs do not have any «CSRF protection», it is possible a malicious 3rd party could access the QRcode and therefore gain access to two-factor authentication codes. | - | ACCESS/NOT_REQUIRED "CSRF protection" |
| GHSA-hmv2-79q8-fv6g | If «percent_encodings» were deduplicated, the time to compute _encode_invalid_chars would be O(kN), where k is at most 484 ((10+6*2)^2). | - | CONFIGURATION/UNCERTAIN "percent_encodings" |
| GHSA-mxh2-ccgj-8635 | On the ESP-IDF platform, ESPHome's web_server authentication check can pass incorrectly when the client-supplied base64-encoded Authorization value is empty or is a substring of the correct value (e.g., «correct usernam… | - | USAGE/UNCERTAIN "correct username with partial password)" |
| GHSA-pxfv-7rr3-2qjg | However, if «copyparty was directly accessible from the internet», then any successful attacks (file retrievals) would unfortunately leave no trace. | - | USAGE/UNCERTAIN "copyparty was directly accessible from the internet" |
| GHSA-v833-3823-cmhp | A control case with «disable_text=True» showed submitted text was not written as a message file, demonstrating the harness was exercising the settings boundary. | - | CONFIGURATION/UNCERTAIN "disable_text=True" |
| GHSA-v833-3823-cmhp | The response and GUI/history accounting can be misleading because the route skips file processing while the «lower-level request stream has already written the file». | - | USAGE/EXCEPTION "lower-level request stream has already written the file" |
