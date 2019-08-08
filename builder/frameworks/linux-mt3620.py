# WizIO 2019 Georgi Angelov
# http://www.wizio.eu/
# https://github.com/Wiz-IO

import os
from os.path import join
from shutil import copyfile
from SCons.Script import ARGUMENTS, DefaultEnvironment, Builder
from subprocess import check_output, CalledProcessError, call, Popen, PIPE
import tempfile
import json

def get_uuid(path):
    t = tempfile.TemporaryFile()
    try:
        output = check_output(path, stderr=t.seek(0))
    except CalledProcessError as e:
        result = e.returncode, t.read()
    else:
        result = 0, output.replace("\r\n", "")
        print '\nUUID: ' + result[1].upper()
    return result[1]

def dev_copy_json(env):
    src = join(env.subst("$PROJECT_DIR"), "src", "app_manifest.json")
    dst = join(env.subst("$BUILD_DIR"), "app_manifest.json")
    copyfile(src, dst)
    uuid = get_uuid( join(env.PioPlatform().get_package_dir("tool-azure"), "uuidgen-64") ) # or 32 
    with open(dst, 'r+') as f:
        data = json.load(f)
        data['ComponentId'] = uuid              # change this
        data['Name'] = "PlatformIO_Application" # change this ProjectName
        data['EntryPoint'] = "/bin/app"         # change this
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
    tool_dir = env.PioPlatform().get_package_dir("tool-azure")
    dst = join(env.subst("$BUILD_DIR"), "app_manifest.json")
    cmd.append( join(tool_dir, "azsphere") ) 
    cmd.append("image")
    cmd.append("package-application")
    cmd.append("--input")
    cmd.append( env.subst("$BUILD_DIR") ) 
    cmd.append("--output")
    cmd.append( join(env.subst("$BUILD_DIR"), "app.image") ) # "manual.imagepackage" 
    cmd.append("--sysroot")
    cmd.append( env.sysroot )
    #cmd.append("--verbose")
    cmd.append("--hardwaredefinition")
    cmd.append( join(env.subst("$PROJECT_DIR"), "src", env.BoardConfig().get("build.variant") + ".json") ) 
    t = tempfile.TemporaryFile()
    try:
        output = check_output(cmd, stderr=t.seek(0))
    except CalledProcessError as e:
        result = e.returncode, t.read()
        print'Pack ERROR: ', result[0], result[1]
    else:
        result = 0, output
        print('\033[1;32;40m'+'PACK ' + result[1])    
    return

def get_exitcode_stdout_stderr(cmd):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out, err
    
def dev_uploader(target, source, env):
    tool_dir = env.PioPlatform().get_package_dir("tool-azure")
    cmd = []
    cmd.append( join(tool_dir, "azsphere") ) 
    cmd.append("device")
    cmd.append("sideload")
    cmd.append("delete")
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    if (0 == exitcode):
        print '\033[1;32;40m'+'DELETED'
    else:
        print '\033[91mERROR', exitcode, "\n", out, err

    cmd = []        
    cmd.append( join(tool_dir, "azsphere") ) 
    cmd.append("device")
    cmd.append("sideload")
    cmd.append("deploy")
    cmd.append("--imagepackage")
    cmd.append(join(env.subst("$BUILD_DIR"), "app.image"))
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    if (0 == exitcode):
        print '\033[1;32;40m'+'UPLOADED'
    else:
        print '\033[91mERROR', exitcode, "\n", out, err    

def dev_create_template(env):
    framework = env.PioPlatform().get_package_dir("framework-azure")
    hardwares = join(framework, "Hardwares")
    templates = join(framework, "Templates")
    core = env.BoardConfig().get("build.variant")
    print "TEMPLATES", templates 
    F = [ 
        join(templates, "main.c"), 
        join(templates, "app_manifest.json"),  
        join(templates, "epoll_timerfd_utilities.c"), 
        join(templates, "epoll_timerfd_utilities.h"),
        join(templates, "applibs_versions.h"),
        join(hardwares, "json", core + ".json"),
        join(hardwares, "inc", core + ".h")
    ]
    for src in F:
        head, fname = os.path.split(src)
        dst = join( env.subst("$PROJECT_DIR"), "src", fname)        
        if False == os.path.isfile( dst ):
            copyfile(src, dst)

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

def dev_init(env, platform):
    dev_create_template(env)
    dev_compiler_poky(env)
    framework_dir = env.PioPlatform().get_package_dir("framework-azure")
    gcc_dir = env.PioPlatform().get_package_dir("toolchain-arm-poky-linux-musleabi-hf")
    env.sysroot = env.BoardConfig().get("build.sysroot", "2") # INI file, default is 2 
    print '\033[1;34;40m'+"AZURE SPHERE SDK SYSROOT:", env.sysroot, "[",env.BoardConfig().get("build.core").upper(),"]", env.BoardConfig().get("build.variant")
    env.Append(
        CPPDEFINES = [ "_POSIX_C_SOURCE" ],        
        CPPPATH = [ 
            join(framework_dir, "Sysroots", env.sysroot, "usr", "include"),        
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")         
        ],        
        CFLAGS = [
            "-O0", "-c",
            "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7", "-std=c11", 
            "--sysroot=" + join(framework_dir, "Sysroots", env.sysroot),
            "-fno-omit-frame-pointer", 
            "-fno-strict-aliasing",  
            "-Wall",    
            "-fno-exceptions",
                                                                   
        ],  
        CXXFLAGS = [                                
            "-fno-rtti",
            "-fno-exceptions", 
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
            "-fno-threadsafe-statics",
        ],  
        CCFLAGS = [
            "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7",                                                                                                    
        ],                     
        LINKFLAGS = [  
            "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7", 
            "--sysroot=" + join(framework_dir, "Sysroots", env.sysroot),
            "-B", gcc_dir,
            "-nodefaultlibs",
            "-Wl,--no-undefined", 
        ],        
        LIBS = [ "applibs", "pthread", "gcc_s", "c"],               
        BUILDERS = dict(
            ElfToBin = Builder(action="", suffix=".1"),
            MakeHeader = Builder( 
                action = env.VerboseAction(dev_pack_image, "Packing image..."),
                suffix = ".bin"
            )  
        ), 
        UPLOADCMD = dev_uploader
    )
    libs = []    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom"), 
            join("$PROJECT_DIR", "lib"),                       
    ))         
    env.Append(LIBS = libs)   





    
