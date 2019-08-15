# WizIO 2019 Georgi Angelov
# http://www.wizio.eu/
# https://github.com/Wiz-IO

import os
import json
import tempfile
from shutil import copyfile
from os.path import join, normpath, basename
from subprocess import check_output, CalledProcessError, call, Popen, PIPE
import uuid
from colorama import Fore

# Windows exe version
def get_uuid(path):
    t = tempfile.TemporaryFile()
    try:
        output = check_output(path, stderr = t.seek(0))
    except CalledProcessError as e:
        result = e.returncode, t.read()
    else:
        result = 0, output.replace("\r\n", "")
        print '\nUUID: ' + result[1].upper()
    return result[1]

def get_exitcode_stdout_stderr(cmd):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    if exitcode != 0:
        print '\n\033[91m' + out, "\n"
        print '\n\033[91m' + err, "\n"
    return exitcode    

def dev_copy_json(env):
    if env.baremetal == False:
        # COPY mt3620.json
        copyfile(
            join(env.framework_dir, "Hardwares", "json", "mt3620.json"), 
            join(env.subst("$BUILD_DIR"), "mt3620.json")
        )
        # COPY VARIANT.json
        file = env.BoardConfig().get("build.variant") + ".json"
        copyfile(
            join(env.framework_dir, "Hardwares", "json", file), 
            join(env.subst("$BUILD_DIR"), file)
        )
    # COPY app_manifest.json
    src = join(env.subst("$PROJECT_DIR"), "src", "app_manifest.json")
    dst = join(env.subst("$BUILD_DIR"), "app_manifest.json")
    copyfile(src, dst)
    U = str(uuid.uuid4()).upper()  # python version
    #U = get_uuid( join(env.tool_dir, "uuidgen-64") )  # exe version: 
    print Fore.BLUE+'UUID: ', U, Fore.BLACK
    with open(dst, 'r+') as f:
        data = json.load(f)
        if env.baremetal == True:
            data['ApplicationType'] = "RealTimeCapable" 
        data['ComponentId'] = U                                                                    # change this
        data['Name'] = "APP_" + basename( normpath( env.subst("$PROJECT_DIR") ) ).replace(" ", "") # change this ProjectName
        data['EntryPoint'] = "/bin/app"                                                            # change this
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate()      

def dev_pack_image(target, source, env):
    bin = join(env.subst("$BUILD_DIR"), "bin")
    try:    os.remove(join(env.subst("$BUILD_DIR"), "app.image"))
    except: pass
    try:    os.remove(join(bin, "app"))
    except: pass   
    try:    os.remove(bin)     
    except: pass
    if False == os.path.isdir(bin):    
        os.makedirs(bin)    
    copyfile(join(env.subst("$BUILD_DIR"), "app.elf"), join(bin, "app"))
    dev_copy_json(env)
    cmd = []
    dst = join(env.subst("$BUILD_DIR"), "app_manifest.json")
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("image")
    cmd.append("package-application")
    cmd.append("--input")
    cmd.append( env.subst("$BUILD_DIR") ) 
    cmd.append("--output")
    cmd.append( join(env.subst("$BUILD_DIR"), "app.image") ) # 
    cmd.append("--sysroot")
    cmd.append( env.sysroot )
    #cmd.append("--verbose")
    if env.baremetal == False:
        print "--hardwaredefinition"
        cmd.append("--hardwaredefinition")
        cmd.append( join(env.subst("$BUILD_DIR"), env.BoardConfig().get("build.variant") + ".json" ) ) # avnet_aesms_mt3620.json
    return get_exitcode_stdout_stderr(cmd)        


def dev_uploader(target, source, env):
    cmd = []
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("device")
    cmd.append("sideload")
    cmd.append("delete")
    if (0 == get_exitcode_stdout_stderr(cmd)):
        print '\033[1;32;40m'+'OLD APPLICATION IS REMOVED'
    else: return
    cmd = []        
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("device")
    cmd.append("sideload")
    cmd.append("deploy")
    cmd.append("--imagepackage")
    cmd.append(join(env.subst("$BUILD_DIR"), "app.image"))
    if (0 == get_exitcode_stdout_stderr(cmd)):
        print '\033[1;32;40m'+'NEW APPLICATION IS READY'
    else: return     

def dev_compiler_poky(env):
    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR="arm-poky-linux-musleabi-ar",
        AS="arm-poky-linux-musleabi-as",
        CC="arm-poky-linux-musleabi-gcc",
        GDB="arm-poky-linux-musleabi-gdb",
        CXX="arm-poky-linux-musleabi-g++",
        OBJCOPY="arm-poky-linux-musleabi-objcopy",
        RANLIB="arm-poky-linux-musleabi-ranlib",
        SIZETOOL="arm-poky-linux-musleabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.bootloader)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGNAME="app",
        PROGSUFFIX=".elf",  
    )      
    env.Append(UPLOAD_PORT='azsphere') #upload_port = "must exist variable"
