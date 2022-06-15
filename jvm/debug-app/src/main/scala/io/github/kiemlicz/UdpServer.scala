package io.github.kiemlicz

import java.net._
import scala.annotation.tailrec
import scala.util.control.NonFatal

// profile and understand the (OS) network buffers, then JVM-level buffers
class UdpServer() {
  private val sock = createSocket()

  private def createSocket(): DatagramSocket = {
    val inetAddress = InetAddress.getByName("192.168.8.170")
    val socket = new MulticastSocket(null)
    val ifc = NetworkInterface.getByInetAddress(inetAddress)
    val socketAddr = new InetSocketAddress(inetAddress, 7777)
    socket.setNetworkInterface(ifc)
    socket.setReuseAddress(false)
    socket.bind(socketAddr) // check if up this point the RST is sent
    socket
  }

  def start(): Unit = {
    // respond with echof
  }
}

class TcpServer() {
  private val sock = createSocket()
  private val accThread = createThread()

  def start() = {
    accThread.start()
  }

  private def createSocket(): ServerSocket = {
    val recvSize = 1024
    val inetAddress = InetAddress.getByName("192.168.8.170")
    val sock = new ServerSocket()
    val socketAddress = new InetSocketAddress(inetAddress, 7777)
    sock.setReceiveBufferSize(recvSize)
    sock.bind(socketAddress)
    sock
  }

  private def createThread(): Thread = {
    new Thread(new Acceptor, "TCP-ACCEPTOR")
  }

  class Acceptor extends Runnable {
    def run(): Unit = {
      @tailrec
      def go(): Unit = if (!sock.isClosed && !Thread.currentThread().isInterrupted()) {
        var clientSocket: Socket = null
        try {
          clientSocket = sock.accept()
          clientSocket.setKeepAlive(true)
          clientSocket.setTcpNoDelay(false)
          clientSocket.setSoLinger(false, -1)
        } catch {
          case NonFatal(e) => e.printStackTrace()
        } finally {
          if (clientSocket != null) clientSocket.close()
        }
        go()
      }

      go()
    }
  }
}

object dpServer {
  def main(args: Array[String]): Unit = {
    val s = new UdpServer()
  }
}