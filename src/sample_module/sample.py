def helloworld(**kwargs):
  if "name" in kwargs:
    name = kwargs["name"]
  else:
    name = "World"
  
  res = f"Hello {name}"
  print(res)
  return res