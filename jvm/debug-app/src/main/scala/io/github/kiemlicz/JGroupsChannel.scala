package io.github.kiemlicz

import org.jgroups.conf.ConfiguratorFactory
import org.jgroups.{JChannel, Message, ObjectMessage, Receiver}

import java.io.{BufferedReader, InputStreamReader}
import scala.annotation.tailrec

object JGroupsChannel extends Receiver {

  override def receive(msg: Message): Unit = {
    val l = msg
    println(l)
  }

  def main(args: Array[String]): Unit = {
    val cfg = args.headOption.getOrElse("tcptest.xml")
    val channel = new JChannel(ConfiguratorFactory.getStackConfigurator(cfg))
    //    val channel = new JChannel()
    channel.connect("testcluster")
    channel.setReceiver(this)
    val in = new BufferedReader(new InputStreamReader(System.in))

    @tailrec
    def stress(): Unit = {
      val dest = null
      val text = ""
      val msg = new ObjectMessage(dest, text)
      channel.send(msg)
      stress()
    }

    @tailrec
    def go(fin: Boolean): Unit = if (!fin) {
      println(">")
      System.out.flush()
      val i = in.readLine().toLowerCase()
      if (i.startsWith("run")) {
        stress()
      } else if (i.startsWith("quit")) {
        go(true)
      }
    }

    go(false)

    channel.close()
  }

}
