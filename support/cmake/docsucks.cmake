

enable_testing()

function(docsucks_test)
    
  # options
    
  set(options )
  set(oneValueArgs )
  set(multiValueArgs PATHS)
  set(prefix _docsucks_test)
  cmake_parse_arguments(${prefix} "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
  
  
endfunction()
