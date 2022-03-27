import random
import time

from .platform import windowMP
from .mouse_utils import (
    move_mouse_and_click,
    move_mouse,
    mouse_position,
    mouse_click,
    mouse_scroll,
    mouse_range,
)
from .debug import debug
from .constants import UIElement, Button, Action
from .image_utils import find_ellement
from .settings import settings_dict
from .game import waitForItOrPass
from .encounter import selectCardsInHand


def collect():
    """Collect the rewards just after beating the final boss of this level"""

    # it's difficult to find every boxes with lib CV2 so,
    # we try to detect just one and then we click on all known positions
    while not find_ellement(Button.done.filename, Action.move_and_click):
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 2.4)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.7, windowMP()[3] / 1.4)

        move_mouse_and_click(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2.7)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.7, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.6, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.8, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.9, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.4, windowMP()[3] / 1.3)
        time.sleep(1)

    # move the mouse to avoid a bug where the it is over a card/hero (at the end)
    # hiding the "OK" button
    move_mouse(windowMP(), windowMP()[2] // 1.25, windowMP()[3] // 1.25)
    # quit the bounty
    while not find_ellement(Button.finishok.filename, Action.move_and_click):
        time.sleep(1)
        mouse_click()
        time.sleep(0.5)


def quitBounty():
    end = False
    if find_ellement(Button.view_party.filename, Action.move_and_click):
        while not find_ellement(UIElement.your_party.filename, Action.move):
            time.sleep(0.5)
        while not find_ellement(Button.retire.filename, Action.move_and_click):
            time.sleep(0.5)
        while not find_ellement(Button.lockin.filename, Action.move_and_click):
            time.sleep(0.5)
        end = True
    return end


def nextlvl():
    """Progress on the map (Boon, Portal, ...) to find the next battle"""
    time.sleep(1.5)

    if not find_ellement(Button.play.filename, Action.screenshot):

        if find_ellement(Button.reveal.filename, Action.move_and_click):
            time.sleep(1)
            move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] // 1.25)
            time.sleep(1.5)

        elif find_ellement(Button.visit.filename, Action.move_and_click):
            y = windowMP()[3] // 2.2
            time.sleep(7)
            while find_ellement(UIElement.visitor.filename, Action.screenshot):
                temp = random.choice([3, 2, 1.7])
                x = windowMP()[2] // temp

                move_mouse_and_click(windowMP(), x, y)

                time.sleep(0.2)
                find_ellement(Button.choose_task.filename, Action.move_and_click)
                time.sleep(0.2)
                mouse_click()
                time.sleep(8)

        elif find_ellement(
            UIElement.pick.filename, Action.move_and_click
        ) or find_ellement(Button.portal_warp.filename, Action.move_and_click):
            time.sleep(1)
            mouse_click()
            time.sleep(5)
        elif find_ellement(UIElement.surprise.filename, Action.screenshot):
            # type A
            time.sleep(1)
            find_ellement(UIElement.surprise.filename, Action.move_and_click)

        elif find_ellement(UIElement.spirithealer.filename, Action.screenshot):
            # type A
            time.sleep(1)
            find_ellement(UIElement.spirithealer.filename, Action.move_and_click)
        else:
            x, y = mouse_position(windowMP())
            debug("Mouse (x, y) : ", x, y)
            if y >= (windowMP()[3] // 2.2 - mouse_range) and y <= (
                windowMP()[3] // 2.2 + mouse_range) :

                x += windowMP()[2] // 25
                if x > windowMP()[2] // 1.5:
                    x = windowMP()[2] // 3.7
            else:
                x = windowMP()[2] // 3.7
            y = windowMP()[3] // 2.2
            debug("move mouse to (x, y) : ", x, y)
            move_mouse_and_click(windowMP(), x, y)


def chooseTreasure():
    """used to choose a Treasure after a battle/fight
    Note: should be updated to select "good" (passive?) treasure instead of a random one
    """
    temp = random.choice([2.3, 1.7, 1.4])
    y = windowMP()[3] // 2
    x = windowMP()[2] // temp
    move_mouse_and_click(windowMP(), x, y)
    time.sleep(0.5)
    while True:
        if find_ellement(Button.take.filename, Action.move_and_click):
            time.sleep(1)
            break
        if find_ellement(Button.keep.filename, Action.move_and_click):
            time.sleep(1)
            break
        if find_ellement(Button.replace.filename, Action.move_and_click):
            time.sleep(1)
            break


def travelpointSelection():
    """Choose a Travel Point (The Barrens, Felwood, ...)
    and the mode : Normal or Heroic
    """

    if find_ellement(UIElement.travelpoint.filename, Action.screenshot):

        move_mouse(windowMP(), windowMP()[2] // 1.5, windowMP()[3] // 2)

        mouse_scroll(50)
        time.sleep(0.5)

        if settings_dict["location"] == "The Barrens":
            find_ellement(UIElement.Barrens.filename, Action.move_and_click)

        elif settings_dict["location"] == "Felwood":
            find_ellement(UIElement.Felwood.filename, Action.move_and_click)

        elif settings_dict["location"] == "Winterspring":
            mouse_scroll(-2)
            move_mouse(windowMP(), windowMP()[2] // 3, windowMP()[3] // 2)
            time.sleep(0.5)
            find_ellement(UIElement.Winterspring.filename, Action.move_and_click)

        elif settings_dict["location"] == "Blackrock":
            mouse_scroll(-10)
            move_mouse(windowMP(), windowMP()[2] // 3, windowMP()[3] // 2)
            time.sleep(0.5)
            find_ellement(UIElement.Blackrock.filename, Action.move_and_click)

        elif settings_dict["location"] == "Alterac":
            mouse_scroll(-15)
            move_mouse(windowMP(), windowMP()[2] // 3, windowMP()[3] // 2)
            time.sleep(0.5)
            find_ellement(UIElement.Alterac.filename, Action.move_and_click)

        else:
            print(
                "[INFO] Travel Point unknown. "
                "The bot won't change the selected travel point."
            )

        move_mouse(windowMP(), windowMP()[2] // 2, windowMP()[3] // 2)
        time.sleep(0.5)

        if settings_dict["mode"] == "Normal":
            find_ellement(UIElement.normal.filename, Action.move_and_click)
        elif settings_dict["mode"] == "Heroic":
            find_ellement(UIElement.heroic.filename, Action.move_and_click)
        else:
            print("[INFO] Settings (for Heroic/Normal) unrecognized.")

    waitForItOrPass(Button.sta, 2)
    find_ellement(Button.sta.filename, Action.move_and_click)


def goToEncounter():
    """
    Start new fight,
    continue on the road and collect everything (treasure, rewards, ...)
    """
    print("goToEncounter : entering")
    time.sleep(2)
    travelEnd = False

    while not travelEnd:
        # ToDo : add a tempo when you detect a new completed task
        # if find (task completed) :
        #   time.sleep(2)

        if find_ellement(Button.play.filename, Action.screenshot):
            if settings_dict["quitbeforebossfight"] == "True" and find_ellement(
                UIElement.boss.filename, Action.screenshot
            ):
                time.sleep(1)
                travelEnd = quitBounty()
                break

            find_ellement(Button.play.filename, Action.move_and_click)

            time.sleep(0.5)
            retour = (
                selectCardsInHand()
            )  # Start the battle : the bot choose the cards and fight against the enemy
            print("goToEncounter - retour = ", retour)
            time.sleep(1)
            if retour == "win":
                print("goToEncounter : battle won")
                while True:
                    if not find_ellement(
                        UIElement.take_grey.filename, Action.screenshot
                    ):
                        mouse_click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if not find_ellement(
                        UIElement.replace_grey.filename, Action.screenshot
                    ):
                        mouse_click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if find_ellement(
                        UIElement.presents_thing.filename, Action.screenshot
                    ):
                        print("goToEncounter : " "Boss defeated. Time for REWARDS !!!")
                        collect()
                        travelEnd = True
                        break
            elif retour == "loose":
                travelEnd = True
                print("goToEncounter : Battle lost")
            else:
                travelEnd = True
                print("goToEncounter : don't know what happened !")
        else:
            nextlvl()
    while not find_ellement(Button.back.filename, Action.screenshot):
        mouse_click()
        time.sleep(1)


def travelToLevel(page="next"):
    """
    Go to a Travel Point, choose a level/bounty and go on the road to make encounter
    """

    retour = False

    if find_ellement(
        f"levels/{settings_dict['location']}"
        f"_{settings_dict['mode']}_{settings_dict['level']}.png",
        Action.move_and_click,
        0.5,
    ):
        waitForItOrPass(Button.start, 6)
        find_ellement(Button.start.filename, Action.move_and_click)
        retour = True
    elif page == "next":
        if find_ellement(Button.sec.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("next")
        if retour is False and find_ellement(
            Button.fir.filename, Action.move_and_click
        ):
            time.sleep(1)
            retour = travelToLevel("previous")
        elif retour is False:
            find_ellement(Button.back.filename, Action.move_and_click)
    elif page == "previous":
        if find_ellement(Button.fir.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("previous")
        else:
            find_ellement(Button.back.filename, Action.move_and_click)
    return retour