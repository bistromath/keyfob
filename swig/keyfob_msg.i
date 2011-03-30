/*
 * First arg is the package prefix.
 * Second arg is the name of the class minus the prefix.
 *
 * This does some behind-the-scenes magic so we can
 * access howto_square_ff from python as howto.square_ff
 */
GR_SWIG_BLOCK_MAGIC(keyfob,msg);

keyfob_msg_sptr keyfob_make_msg (gr_msg_queue_sptr queue, double rate, double threshold);

class keyfob_msg : public gr_sync_block
{
private:
  keyfob_msg (gr_msg_queue_sptr queue, double rate, double threshold);
};
