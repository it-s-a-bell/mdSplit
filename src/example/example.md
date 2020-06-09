---
title: Dypsloom Character Controller
date: 06/07/2020
author: John Doe
---

## Introduction

The Dypsloom Character Controller is an Unity asset that offers a simple yet powerful set of
character scripts. It’s primary use case is to quickly create game prototypes. It offers features
such as taking and dealing damage, dying/respawning, interaction, moving platforms, picking
up, dropping and equipping items, etc....
The implementation of these features are simple which means they are a bit limited. That being
said the code is well structured and fully documented. Therefore it can easily be extended to
your own needs with a bit of custom code.


## Content

The asset contains the following:
- The Dyp character model with textures, shaders and effects
- The Environment, including Ice platforms, Water, Ice crystals, a pickaxe and a fish
- The scripts include a pool manager, damageable, interactable, UsabelItem, etc...
- A demo scene with a mini game where Dyp needs to find the fish
The asset requires:
- TextMeshPro
- Built-in or URP render pipelines
The asset does not support
- HDRP
This asset integrates with:
- URP
- TextMeshPro
- Cinemachine
- Boar hunter

## Getting started

The best way to get started is by trying out the demo scene. By checking the game objects in
the scene and the components attached to them you’ll get an idea of how components interact
with each other.


When starting a new scene you can drag and drop the “Dyp” character prefab into a scene to
get started right away. You may also add the “Character UI” prefab to view your character
health and items.
From there you can block out a level with primitive shapes and/or prefabs from the asset. You
may add simple components such as “Interactable” or “Damageable” to make your scene more
dynamic.
Using the video tutorials and this documentation you’ll learn how to take advantage of each
component and even extend them to fit your exact needs.

## The basics

Before getting started with the asset it is important to learn the basics of coding in Unity.

### Monobehaviours, Classes, Structs and Interfaces

To take the full advantage of the asset it is important to learn the basics of C# and the Unity
API. There are many great tutorials out there so I will give a brief explanation here and you may
look for more details online if you need to.

#### Monobehaviours

Monobehaviour is a class within the Unity API that is used to create components. Components
are logic that you can attach to a gameobject. They have useful methods which are called by
Unity itself such as Awake, Start, Update, OnTriggerEnter, OnTriggerExit, etc... You may find all
those methods and the order in which they are called here:
https://docs.unity3d.com/Manual/ExecutionOrder.html
Usually monobehaviours are used whenever you need logic that interacts with the game world
such as “Character” or “MovingPlatform”. It is good practice to keep your monobehaviours
simple and modular so that they can be reused in different circumstances.
```
public​ ​class​ ​ItemPickup​ : ​MonoBehaviour
{
}
```

#### Classes

Classes define a type of object. Each object of a class has a reference which makes it unique.
An example for a class is “Animal”. An class can have subclasses which we call inheritors. For
the case of “Animal” we could have a sub-class “Penguin”, “Pig”, etc... objects can be created
from a class for example you could make a Penguin object call it “Dyp” and another Penguin
object and called it “Sloom”.
As mentioned before Monobehaviour is a class and by default when creating a script in Unity it
will have a template that automatically makes the script inherit Monobehaviour. You do not have
to derive from Monobehaviour, if you wish you can derive from other classes, or from nothing.
```
public​ ​class​ ​CharacterRotator
{
}
```
#### Structs

Structs are used to group values and objects together. The way the are written is similar to a
class. They function very differently though. A struct cannot inherit from another struct. Structs
do not create objects they create values, therefore they are saved on the stack and not the
heap, which can reduce garbage collection. The tradeoff is that modifying the struct value will
only work on the local scope of the code, therefore struct should in principle be immutable. If
you do not know about stack, heaps, garbage collection, etc... you may research about it but it
is not required to understand them to create game prototypes or simple games in general.
```
[​Serializable​]
public​ ​struct​ ItemAmount
{
[​SerializeField​] ​private​ Item m_Item;
[​SerializeField​] ​private​ ​int​ m_Amount;
​public​ ​int​ Amount => m_Amount;
​public​ Item Item => m_Item;
​public​ ​ItemAmount​(Item item, ​int​ amount)
{
m_Amount = amount;
m_Item = item;
}
​public​ ​static​ ​implicit​ ​operator​ ​ItemAmount​( (​int​,Item) x)
=> ​new​ ItemAmount(x.Item2,x.Item1);
​public​ ​static​ ​implicit​ ​operator​ ​ItemAmount​( (Item,​int​) x)
=> ​new​ ItemAmount(x.Item1,x.Item2);
}
```
#### Interfaces

Interfaces define a contract that any class or struct that inherits it needs to abide to. In an
interface you may define the public setters/getters, methods and events that the inheritors need
to implement.
By using an interface you no longer care whether an object has class A, B or C, you only care
that you can call a specific method on that object. Interface are useful for very generic
functionality such as interaction or damaging.
```
public​ ​interface​ ​IInteractable
{
​bool​ IsInteractable { ​get​; }
​bool​ ​Interact​(IInteractor interactor);
​bool​ ​Select​(IInteractor interactor);
​bool​ ​Unselect​(IInteractor interactor);
}
```

## Character

The character script is a monobehaviour which is used to group the scripts that will control the
character. The control scripts are each used to control a very specific piece of the character. For
example we have the Character mover which is used to move the character and the Character
Rotator which only deals with rotating the character. Keeping these controls modular and well
separated allows you to swap them out by something else without having to change code all
over the place.
For people who do not want to write a line of code, you are free to use the components
available within the demo. But for those who are ready to give it a shot, try adding a new
character control and you’ll find that it is easier than you’d think thanks to the way the character
script is organized.
You’ll find video tutorials on this subject on our Youtube channel.
Most beginner Unity programmers believe that you must write a Monobehaviour and put all your
logic in one big Update function so that it can be processed on each frame. This can become
quickly very messy. To keep things clean you can instead use the “Tick” pattern, which consists
of calling a Tick function on a class within the Monobehaviour Update function like so:
```
protected​ ​virtual​ ​void​ ​Update​()
{
m_CharacterMover.Tick();
m_CharacterRotator.Tick();
}
```
This way the character control script can run logic every frame without being a monobehaviour.

### Setting up a Character

For the character script to work correctly you’ll need to add an animator and make sure the
Apply RootMotion is off.
You should also add a rigidbody, it must be set as kinematic. Gravity is set on the character
mover.
The Character controller is also required as it is used by the default Character Mover script.
Here is an example of the character in the inspector:



### Character Mover

The default character mover is used to move the character respective to the camera. It takes in
a speed value to change the movement speed of the character.

IMAGE

### Character Rotator

The default character rotator rotates the character in the direction of the input. This allows the
character to always look where it is trying to go.

### Character Input

The character input allows you to map actions to inputs. You’ll most likely need to add your own
if you wish to extend functionality.
```
public​ ​interface​ ​ICharacterInput​ : ​IItemInput
{
​float​ Horizontal { ​get​; }
​float​ Vertical { ​get​; }
​bool​ Interact { ​get​; }
}
```

### Character Animator

The character animator will animate the character depending on the state of the other character
controls. Example: animate the character moving when the character mover is moving the
character.

## Interactors and Interactables

Interactors and Interactables interfaces are used for components to interact with each other.
Interactors can select, unselect and interact with interactables. When the interactable is
selected, unselected or interacted with it sends an event, which you can use to do any number
of interesting things. You could interact with an object to pick up an item or action a lever that
opens a path, etc...
Usually an interactable will be paired with an InteractableBehaviour which defines what happens
when the interactable is interacted with. You can write your own InteractableBehaviours to
create custom features. You can also use the Unity Actions directly in the inspector to trigger
some functions on interaction without writing a line of code.

IMAGE

## Damageable

The damageable interface is used by objects or characters to take damage, heal and die. You
can listen to those events to add functionality. For example whenever a character's health
changes when taking damage or healing I update the health slider with the HealthMonitor.
When you want to damage a damageable it is as simple as to write:
```
damageable.TakeDamage(damage);
```
IMAGE 

Or you can insta-kill a damageable with:

```
damageable.Die();
```
When dying a character will respawn at a spawn point specified in the inspector.

## Inventory

The inventory is used to keep track of the items picked up by the character. It is also used to
equip items and use them.
IMAGE

### Item Definition

The item definition is a scriptable object that contains data about an item, such as its name,
icon, etc... Using scriptable objects makes it very easy to create items and organize them.
When an item is spawned you can use the itemDefinition to tell if the items are similar. If the
item is flagged as not unique the items can be stacked.

### Item

The item is a gameobject that is bound to an ItemDefinition. Items are prefabs that can easily be
instantiated in the scene with different components.

## Camera

The character controller offers two types of cameras. The first camera follows the character from
a fixed offset. Perfect for top down games or 2.5D games.
IMAGE

The second is can be used only if you have cinemachine and it lets you rotate the camera
around the player.

## User Interface

The UI is simple and mostly consists of monitors that lets you view information about your
player. For example we have a health monitor which listens to events on the character
damageable component to update the slider.

### Hot Item Bar

The hot item bar allows you to see the items that your character has. You can use/equip/drop
the items you want once the character picks them up. Use the keys 1-9 to use items in the hot
bar or equip them if they are equippable. Use ctrl+key or ctrl+mouse click to drop the item.

IMAGE

