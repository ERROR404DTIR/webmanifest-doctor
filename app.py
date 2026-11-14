#!/usr/bin/env python3
"""Validate a Progressive Web App web app manifest."""
import argparse,json
from pathlib import Path
from urllib.parse import urlparse
def validate(data):
 issues=[]
 def add(level,msg):issues.append({"level":level,"message":msg})
 if not isinstance(data,dict):return {"issues":[{"level":"error","message":"manifest root must be an object"}]}
 if not data.get("name") and not data.get("short_name"):add("error","provide name or short_name")
 if not isinstance(data.get("start_url"),str) or not data["start_url"]:add("error","start_url is required")
 if data.get("display","") not in ("fullscreen","standalone","minimal-ui","browser"):add("warning","display is missing or not a recognized value")
 for color in ("theme_color","background_color"):
  if color in data and (not isinstance(data[color],str) or not data[color].startswith("#")):add("warning",color+" should be a CSS hex color")
 icons=data.get("icons",[])
 if not isinstance(icons,list):add("error","icons must be an array");icons=[]
 if not icons:add("warning","no icons declared")
 for i,icon in enumerate(icons):
  if not isinstance(icon,dict):add("error",f"icons[{i}] must be an object");continue
  if not icon.get("src"):add("error",f"icons[{i}] has no src")
  if not icon.get("sizes"):add("warning",f"icons[{i}] has no sizes")
  if not icon.get("type"):add("warning",f"icons[{i}] has no MIME type")
  if icon.get("purpose") and not set(icon["purpose"].split())<= {"any","maskable","monochrome"}:add("warning",f"icons[{i}] has an unknown purpose")
 scope=data.get("scope");start=data.get("start_url")
 if scope and start:
  s=urlparse(scope);u=urlparse(start)
  if s.scheme and u.scheme and (s.scheme,s.netloc)!=(u.scheme,u.netloc):add("error","start_url and scope use different origins")
  if s.path and u.path and not u.path.startswith(s.path):add("warning","start_url appears outside the declared scope")
 shortcuts=data.get("shortcuts",[])
 if not isinstance(shortcuts,list):add("warning","shortcuts should be an array")
 else:
  for i,x in enumerate(shortcuts):
   if not isinstance(x,dict) or not x.get("name") or not x.get("url"):add("warning",f"shortcut {i} needs name and url")
 return {"issues":issues,"errors":sum(x["level"]=="error" for x in issues),"warnings":sum(x["level"]=="warning" for x in issues)}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("manifest",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args()
 try:data=json.loads(a.manifest.read_text(encoding="utf-8"))
 except (OSError,json.JSONDecodeError) as e:p.error(str(e))
 r=validate(data)
 if a.json:print(json.dumps(r,indent=2));return
 print(f"Errors: {r['errors']} · Warnings: {r['warnings']}")
 for x in r["issues"]:print(x["level"].upper()+": "+x["message"])
 if not r["issues"]:print("Manifest looks structurally healthy.")
if __name__=="__main__":main()
