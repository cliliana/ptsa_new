#emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
#ex: set sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See the COPYING file distributed along with the PTSA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

# from numpy import *
import numpy as np
import os.path

def reshape_to_2d(data,axis):
    """Reshape data to 2D with specified axis as the 2nd dimension."""
    # get the shape, rank, and the length of the chosen axis
    dshape = data.shape
    rnk = len(dshape)
    n = dshape[axis]
    # convert negative axis to positive axis
    if axis < 0: 
        axis = axis + rnk
    # determine the new order of the axes
    newdims = np.r_[0:axis,axis+1:rnk,axis]

    # reshape and transpose the data
    newdata = np.reshape(np.transpose(data,tuple(newdims)),
                         (np.prod(dshape,axis=0)/n,n))

    # make sure we have a copy
    #newdata = newdata.copy()

    return newdata

def reshape_from_2d(data,axis,dshape):
    """Reshape data from 2D back to specified dshape."""

    # set the rank of the array
    rnk = len(dshape)

    # fix negative axis to be positive
    if axis < 0: 
        axis = axis + rnk

    # determine the dims from reshape_to_2d call
    newdims = np.r_[0:axis,axis+1:rnk,axis]

    # determine the transposed shape and reshape it back
    tdshape = np.take(dshape,newdims,0)
    ret = np.reshape(data,tuple(tdshape))

    # figure out how to retranspose the matrix
    vals = range(rnk)
    olddims = vals[:axis] + [rnk-1] +vals[axis:rnk-1]
    ret = np.transpose(ret,tuple(olddims))

    # make sure we have a copy
    #ret = ret.copy()
    return ret

def repeat_to_match_dims(x,y,axis=-1):

    rnk = len(y.shape)

    # convert negative axis to positive axis
    if axis < 0: 
        axis = axis + rnk

    for d in range(axis)+range(axis+1,rnk):
        # add the dimension
        x = np.expand_dims(x,d)
        # repeat to fill that dim
        x = x.repeat(y.shape[d],d)

    return x


def deg2rad(degrees):
    """Convert degrees to radians."""
    return degrees/180.*np.math.pi

def rad2deg(radians):
    """Convert radians to degrees."""
    return radians/np.math.pi*180.

def pol2cart(theta,radius,z=None,radians=True):
    """Converts corresponding angles (theta), radii, and (optional) height (z)
    from polar (or, when height is given, cylindrical) coordinates
    to Cartesian coordinates x, y, and z.
    Theta is assumed to be in radians, but will be converted
    from degrees if radians==False."""
    if radians:
        x = radius*np.cos(theta)
        y = radius*np.sin(theta)
    else:
        x = radius*np.cos(deg2rad(theta))
        y = radius*np.sin(deg2rad(theta))
    if z is not None:
        # make sure we have a copy
        z=z.copy()
        return x,y,z
    else:
        return x,y

def cart2pol(x,y,z=None,radians=True):
    """Converts corresponding Cartesian coordinates x, y, and (optional) z
    to polar (or, when z is given, cylindrical) coordinates
    angle (theta), radius, and z.
    By default theta is returned in radians, but will be converted
    to degrees if radians==False."""    
    if radians:
        theta = np.arctan2(y,x)
    else:
        theta = rad2deg(np.arctan2(y,x))
    radius = np.hypot(x,y)
    if z is not None:
        # make sure we have a copy
        z=z.copy()
        return theta,radius,z
    else:
        return theta,radius

def lock_file(filename,lockdirpath=None,lockdirname=None):
    if lockdirname is None:
        lockdirname=filename+'.lock'
    if not(lockdirpath is None):
        lockdirname = lockdirpath+lockdirname
    if os.path.exists(lockdirname):
        return False
    else:
        try:
            os.mkdir(lockdirname)
        except:
            return False
    return True

def release_file(filename,lockdirpath=None,lockdirname=None):
    if lockdirname is None:
        lockdirname=filename+'.lock'
    if not(lockdirpath is None):
        lockdirname = lockdirpath+lockdirname
    try:
        os.rmdir(lockdirname)
    except:
        return False
    return True

def next_pow2(n):
    """
    Returns p such that 2 ** p >= n
    """
    p = int(np.floor(np.log2(n)))
    if 2 **  p == n:
        return p
    else:
        return p + 1

def pad_to_next_pow2(x, axis=0):
    """
    Pad an array with zeros to the next power of two along the
    specified axis.

    Note: This is much easier with numpy version 1.7.0, which has a
    new pad method.
    """
    cur_len = x.shape[axis]
    new_len = 2 ** next_pow2(cur_len)
    to_pad = new_len - cur_len
    if to_pad > 0:
        shape = list(x.shape)
        shape[axis] = to_pad
        padding = np.zeros(shape, dtype=x.dtype)
        return np.concatenate([x,padding], axis=axis)
    else:
        # nothing needs to be done
        return x


def centered(arr, newsize):
    """
    Return the center newsize portion of the input array.

    Parameters
    ----------
    arr : {array}
        Input array
    newsize : {tuple of ints}
        A tuple specifing the size of the new array.

    Returns
    -------
    A center slice into the input array

    Note
    ----
    Adapted from scipy.signal.signaltools._centered

    """
    # Don't make a copy of newsize when creating array:
    newsize = np.asarray(newsize)
    # Do make a copy of arr.shape when creating array:
    currsize = np.array(arr.shape)
    # determine start- & end-indices and slice:
    startind = (currsize - newsize) / 2
    endind = startind + newsize
    myslice = [slice(startind[k], endind[k]) for k in range(len(endind))]
    return arr[tuple(myslice)]


import inspect
def getargspec(obj):
    """Get the names and default values of a callable's
       arguments

    A tuple of four things is returned: (args, varargs,
    varkw, defaults).
      - args is a list of the argument names (it may
        contain nested lists).
      - varargs and varkw are the names of the * and
        ** arguments or None.
      - defaults is a tuple of default argument values
        or None if there are no default arguments; if
        this tuple has n elements, they correspond to
        the last n elements listed in args.

    Unlike inspect.getargspec(), can return argument
    specification for functions, methods, callable
    objects, and classes.  Does not support builtin
    functions or methods.

    See http://kbyanc.blogspot.com/2007/07/python-more-generic-getargspec.html
    """
    if not callable(obj):
        raise TypeError("%s is not callable" % type(obj))
    try:
        if inspect.isfunction(obj):
            return inspect.getargspec(obj)
        elif hasattr(obj, 'im_func'):
            # For methods or classmethods drop the first
            # argument from the returned list because
            # python supplies that automatically for us.
            # Note that this differs from what
            # inspect.getargspec() returns for methods.
            # NB: We use im_func so we work with
            #     instancemethod objects also.
            spec = list(inspect.getargspec(obj.im_func))
            spec[0] = spec[0][1:]
            return spec
        elif inspect.isclass(obj):
            return getargspec(obj.__init__)
        elif isinstance(obj, object) and \
             not isinstance(obj, type(arglist.__get__)):
            # We already know the instance is callable,
            # so it must have a __call__ method defined.
            # Return the arguments it expects.
            return getargspec(obj.__call__)
    except NotImplementedError:
        # If a nested call to our own getargspec()
        # raises NotImplementedError, re-raise the
        # exception with the real object type to make
        # the error message more meaningful (the caller
        # only knows what they passed us; they shouldn't
        # care what aspect(s) of that object we actually
        # examined).
        pass
    raise NotImplementedError("do not know how to get argument list for %s" % \
          type(obj))
