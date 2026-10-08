add_rules("mode.debug", "mode.release")
option("egp_cpp_sdk") set_showmenu(true) option_end()
local sdk = get_config("egp_cpp_sdk")
if sdk then includes(path.join(sdk, "xmake.lua")) end
target("extension")
    set_kind("shared")
    set_languages("cxx17")
    if is_plat("windows") then
        set_runtimes(is_mode("debug") and "MDd" or "MD")
        set_prefixname("")
    else
        set_prefixname("lib")
    end
    local platform = is_plat("macosx") and "macos" or get_config("plat")
    local architecture = get_config("arch") == "x64" and "x86_64" or get_config("arch")
    local mode = is_mode("debug") and "template_debug" or "template_release"
    local suffix = is_plat("macosx") and "" or "." .. architecture
    set_basename("gdexample." .. platform .. "." .. mode .. suffix)
    set_targetdir("project/bin")
    add_files("src/*.cpp")
    add_includedirs("src")
    add_deps("godot-cpp")
target_end()
