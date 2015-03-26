from thinc.typedefs cimport atom_t

from ._state cimport State


cdef int fill_context(atom_t* context, State* state) except -1
# Context elements

# Ensure each token's attributes are listed: w, p, c, c6, c4. The order
# is referenced by incrementing the enum...

# Tokens are listed in left-to-right order.
#cdef size_t* SLOTS = [
#    S2w, S1w,
#    S0l0w, S0l2w, S0lw,
#    S0w,
#    S0r0w, S0r2w, S0rw,
#    N0l0w, N0l2w, N0lw,
#    P2w, P1w,
#    N0w, N1w, N2w, N3w, 0
#]

# NB: The order of the enum is _NOT_ arbitrary!!
cpdef enum:
    S2w
    S2W
    S2p
    S2c
    S2c4
    S2c6
    S2L
    S2_prefix
    S2_suffix
    S2_shape

    S1w
    S1W
    S1p
    S1c
    S1c4
    S1c6
    S1L
    S1_prefix
    S1_suffix
    S1_shape

    S1rw
    S1rW
    S1rp
    S1rc
    S1rc4
    S1rc6
    S1rL
    S1r_prefix
    S1r_suffix
    S1r_shape

    S0lw
    S0lW
    S0lp
    S0lc
    S0lc4
    S0lc6
    S0lL
    S0l_prefix
    S0l_suffix
    S0l_shape

    S0l2w
    S0l2W
    S0l2p
    S0l2c
    S0l2c4
    S0l2c6
    S0l2L
    S0l2_prefix
    S0l2_suffix
    S0l2_shape

    S0w
    S0W
    S0p
    S0c
    S0c4
    S0c6
    S0L
    S0_prefix
    S0_suffix
    S0_shape
    
    S0r2w
    S0r2W
    S0r2p
    S0r2c
    S0r2c4
    S0r2c6
    S0r2L
    S0r2_prefix
    S0r2_suffix
    S0r2_shape

    S0rw
    S0rW
    S0rp
    S0rc
    S0rc4
    S0rc6
    S0rL
    S0r_prefix
    S0r_suffix
    S0r_shape

    N0l2w
    N0l2W
    N0l2p
    N0l2c
    N0l2c4
    N0l2c6
    N0l2L
    N0l2_prefix
    N0l2_suffix
    N0l2_shape

    N0lw
    N0lW
    N0lp
    N0lc
    N0lc4
    N0lc6
    N0lL
    N0l_prefix
    N0l_suffix
    N0l_shape

    N0w
    N0W
    N0p
    N0c
    N0c4
    N0c6
    N0L
    N0_prefix
    N0_suffix
    N0_shape
 
    N1w
    N1W
    N1p
    N1c
    N1c4
    N1c6
    N1L
    N1_prefix
    N1_suffix
    N1_shape

    N2w
    N2W
    N2p
    N2c
    N2c4
    N2c6
    N2L
    N2_prefix
    N2_suffix
    N2_shape
  
    P1w
    P1W
    P1p
    P1c
    P1c4
    P1c6
    P1L
    P1_prefix
    P1_suffix
    P1_shape
    
    P2w
    P2W
    P2p
    P2c
    P2c4
    P2c6
    P2L
    P2_prefix
    P2_suffix
    P2_shape
   
    # Misc features at the end
    dist
    N0lv
    S0lv
    S0rv
    S1lv
    S1rv

    S0_has_head
    S1_has_head
    S2_has_head

    CONTEXT_SIZE
