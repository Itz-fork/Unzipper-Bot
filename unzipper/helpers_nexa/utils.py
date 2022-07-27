# ===================================================================== #
#                      Copyright (c) 2022 Itz-fork                      #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  #
# See the GNU General Public License for more details.                  #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>   #
# ===================================================================== #

# Credits: SpEcHiDe's AnyDL-Bot for progress_for_pyrogram, humanbytes and TimeFormatter

from re import sub
from time import time
from math import floor
from json import loads
from os import path, walk
from functools import partial
from subprocess import Popen, PIPE
from asyncio import get_running_loop


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time()
    diff = now - start
    speed = current / diff
    if total:
        if round(diff % 10.00) == 0 or current == total:
            percentage = current * 100 / total
            elapsed_time = round(diff) * 1000
            estimated_total_time = elapsed_time + \
                round((total - current) / speed) * 1000

            elapsed_time = TimeFormatter(elapsed_time)
            estimated_total_time = TimeFormatter(estimated_total_time)

            progress = "[{0}{1}] \n**📊 Progress**: {2}%\n".format(
                # Filled
                ''.join(["◉" for i in range(floor(percentage / 5))]),
                # Empty
                ''.join(["◎" for i in range(20 - floor(percentage / 5))]),
                round(percentage, 2))

            tmp = progress + "{0} of {1}\n**🏃 Speed:** {2}/s\n**⏰ ETA:** {3}\n".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                estimated_total_time if estimated_total_time != '' else "0 s"
            )
            try:
                await message.edit("{}\n {} \n\n**Powered by @NexaBotsUpdates**".format(ud_type, tmp))
            except:
                pass
    else:
        tmp = "**📊 Progress:** {0} of {1}\n**🏃 Speed:** {2}/s\n**⏰ ETA:** {3}\n".format(
            humanbytes(current),
            "?",
            humanbytes(speed),
            "unknown"
        )
        try:
            await message.edit("{}\n {} \n\n**Powered by @NexaBotsUpdates**".format(ud_type, tmp))
        except:
            pass


def humanbytes(size: int):
    if not size:
        return "N/A"
    power = 2**10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2] if tmp[:-2] else "0ms"


def run_shell_cmds(command):
    """
    Execute shell commands and returns the output
    """
    run = Popen(command, stdout=PIPE,
                stderr=PIPE, shell=True)
    shell_ouput = run.stdout.read()[:-1].decode("utf-8")
    return shell_ouput


async def run_cmds_on_cr(func, *args, **kwargs):
    """
    Execute blocking functions asynchronously
    """
    loop = get_running_loop()
    return await loop.run_in_executor(
        None,
        partial(func, *args, **kwargs)
    )


async def get_files(fpath: str, filter_fn=None):
    """
    Returns files in a folder

    Parameters:

        - `fpath` - Path to the folder
        - `filter_fn` - Function to filter elements in the array
    """
    path_list = [val for sublist in [
        [path.join(i[0], j) for j in i[2]] for i in walk(fpath)] for val in sublist]
    if filter_fn:
        path_list = list(filter(filter_fn, path_list))
    return sorted(path_list)


def read_json_sync(name: str, as_items: bool = False) -> dict:
    """
    Reads json file and returns a dict

    Parameters:

        - `name` - File path
        - `as_items` - Pass "True" if you want to return items of the dict
    """
    with open(name) as fs:
        return loads(fs.read()).items() if as_items else loads(fs.read())


async def rm_mark_chars(text: str):
    """
    Remove basic markdown characters

    Parameters:

        - `text` - Text
    """
    return sub("[*`_]", "", text)
