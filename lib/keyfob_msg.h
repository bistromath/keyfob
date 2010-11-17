/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */
#ifndef INCLUDED_keyfob_msg_H
#define INCLUDED_keyfob_msg_H

#include <gr_sync_block.h>
#include <gr_msg_queue.h>

class keyfob_msg;

/*
 * We use boost::shared_ptr's instead of raw pointers for all access
 * to gr_blocks (and many other data structures).  The shared_ptr gets
 * us transparent reference counting, which greatly simplifies storage
 * management issues.  This is especially helpful in our hybrid
 * C++ / Python system.
 *
 * See http://www.boost.org/libs/smart_ptr/smart_ptr.htm
 *
 * As a convention, the _sptr suffix indicates a boost::shared_ptr
 */
typedef boost::shared_ptr<keyfob_msg> keyfob_msg_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of keyfob_msg.
 *
 * To avoid accidental use of raw pointers, keyfob_msg's
 * constructor is private.  howto_make_square_ff is the public
 * interface for creating new instances.
 */
keyfob_msg_sptr keyfob_make_msg (gr_msg_queue_sptr queue, double rate, double threshold);

/*!
 * \brief square a stream of floats.
 * \ingroup block
 *
 * \sa howto_square2_ff for a version that subclasses gr_sync_block.
 */
class keyfob_msg : public gr_sync_block
{
private:
  // The friend declaration allows howto_make_square_ff to
  // access the private constructor.

  friend keyfob_msg_sptr keyfob_make_msg (gr_msg_queue_sptr queue, double rate, double threshold);

  keyfob_msg (gr_msg_queue_sptr queue, double rate, double threshold);  	// private constructor
  gr_msg_queue_sptr d_queue; //our queue
  double d_rate;
  double d_threshold;
  double d_bitrate_min;
  double d_bitrate_max;
  double d_bitrate;
  double d_bitrate_step;
  double d_samples_per_bit;
  

 public:
  ~keyfob_msg ();	// public destructor

  // Where all the action really happens

  int work (int noutput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_keyfob_msg_H */
