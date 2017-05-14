# Sublime Text - PyCommont

A sublime text plugin. Generate docstring comments into python function.

before:

```python
def test(self, edit, forward=False, point=(10,20)):
    pass
```

after:

```python
def test(self, edit, forward=False, point=(10,20)):
    """
    
    Args:
      edit -- 
      forward -- 
      point -- 
    Returns: 
    Raises: 
    """
    pass
```

### installation

Open Packages folder:  `Preferences >> Browse Packages `

Put pycomment folder into Packages folder.

### key bindings

`alt+y`

You can set your own key by editing `sublime-keymap` file.

