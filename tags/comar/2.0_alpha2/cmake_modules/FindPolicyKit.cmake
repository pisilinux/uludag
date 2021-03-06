FILE (GLOB PK_LIBRARY /usr/lib/libpolkit-grant.so.2.*)

IF (PK_LIBRARY)
    SET (HAVE_POLICYKIT TRUE)
ENDIF (PK_LIBRARY)

IF (HAVE_POLICYKIT)
   IF (NOT PolicyKit_FIND_QUIETLY)
      MESSAGE (STATUS "Found PolicyKit")
   ENDIF (NOT PolicyKit_FIND_QUIETLY)
ELSE (HAVE_POLICYKIT)
   IF (PolicyKit_FIND_REQUIRED)
      MESSAGE (FATAL_ERROR "Could not find PolicyKit.")
   ELSE (PolicyKit_FIND_REQUIRED)
      MESSAGE (STATUS "Could not find PolicyKit. Access control feature will be disabled.")
   ENDIF (PolicyKit_FIND_REQUIRED)
ENDIF (HAVE_POLICYKIT)
