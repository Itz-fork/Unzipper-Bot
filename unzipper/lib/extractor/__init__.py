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

from os import path, mkdir
from .errors import ExtractionFailed
from unzipper.helpers_nexa.utils import run_shell_cmds, run_cmds_on_cr


class Extractor:
    """
    Unzip archives using 7z and zstd
    """

    def __init__(self) -> None:
        pass

    async def extract(self, arc_path: str, out: str, password: str = "", splitted: bool = False):
        """
        Extract archive using either 7z or zstd

        Parameters:

            - `arc_path` - Archive path
            - `out` - Output path
            - `password` - Password to use incase if the archive is password protected
            - `splitted` - Pass True if the archive is a splitted archive which usually ends with .001 (+) extensions
        """
        if path.splitext(arc_path)[1] == ".zst":
            mkdir(out)
            ex = await self._ext_zstd(out, arc_path)
            await self.__check_output(ex)
            return ex
        else:
            ex = await self._ext_7z(out, arc_path, password, splitted)
            await self.__check_output(ex)
            return ex

    async def _ext_7z(self, out: str, arc_path: str, password: str = "", splitted: bool = False):
        if password:
            command = f"7z x -o\"{out}\" -p\"{password}\" \"{arc_path}\" -y"
        else:
            command = f"7z x -o\"{out}\" \"{arc_path}\" -y"
        command += " -tsplit" if splitted else ""
        return await run_cmds_on_cr(run_shell_cmds, command)

    async def _ext_zstd(self, out: str, arc_path: str):
        command = f"zstd -f --output-dir-flat \"{out}\" -d \"{arc_path}\""
        return await run_cmds_on_cr(run_shell_cmds, command)

    async def __check_output(self, out: str):
        if any(e in out for e in ["Error", "Can't open as archive"]):
            raise ExtractionFailed
