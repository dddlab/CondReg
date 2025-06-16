.onLoad <- function(libname, pkgname) {
  # Load the compiled library
  library.dynam("condregR", pkgname, libname)
}

.onUnload <- function(libpath) {
  # Unload the compiled library
  library.dynam.unload("condregR", libpath)
} 